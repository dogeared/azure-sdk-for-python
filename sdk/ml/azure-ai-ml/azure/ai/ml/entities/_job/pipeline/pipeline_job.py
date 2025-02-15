# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
from typing import Dict, Union, Optional

from azure.ai.ml._schema.pipeline import PipelineJobSchema
from azure.ai.ml.entities._job.automl.automl_job import AutoMLJob
from azure.ai.ml.entities._builders.parallel import Parallel
from azure.ai.ml.entities._job.pipeline._io import (
    PipelineIOMixin,
    OutputsAttrDict,
    InputsAttrDict,
)
from azure.ai.ml.entities._builders import Sweep, Command, BaseNode
from azure.ai.ml._utils.utils import (
    snake_to_camel,
    camel_to_snake,
    transform_dict_keys,
    is_data_binding_expression,
    is_private_preview_enabled,
)
from azure.ai.ml._restclient.v2022_02_01_preview.models import (
    JobBaseData,
    JobOutput as RestJobOutput,
    PipelineJob as RestPipelineJob,
    ManagedIdentity,
    UserIdentity,
    AmlToken,
)
from azure.ai.ml.constants import BASE_PATH_CONTEXT_KEY, ComponentSource, NodeType, AZUREML_PRIVATE_FEATURES_ENV_VAR
from azure.ai.ml.entities._inputs_outputs import Input, Output
from azure.ai.ml.entities._job.pipeline.pipeline_job_settings import PipelineJobSettings
from azure.ai.ml.entities._job.job import Job
from azure.ai.ml.entities._component.component import Component
from azure.ai.ml.entities._component._pipeline_component import _PipelineComponent
from azure.ai.ml.entities._job._input_output_helpers import (
    to_rest_dataset_literal_inputs,
    to_rest_data_outputs,
    from_rest_inputs_to_dataset_literal,
    from_rest_data_outputs,
)
from azure.ai.ml.entities._job.pipeline._exceptions import UserErrorException
from azure.ai.ml.entities._mixins import YamlTranslatableMixin
from azure.ai.ml.entities._util import load_from_dict
from azure.ai.ml.entities._schedule.schedule import CronSchedule, RecurrenceSchedule, Schedule

from azure.ai.ml._ml_exceptions import ValidationException, ErrorCategory, ErrorTarget


class PipelineJob(Job, YamlTranslatableMixin, PipelineIOMixin):
    """
    Pipeline job. Please use @pipeline decorator to create a PipelineJob, not recommended instantiating it directly.

    :param component: Pipeline component version. Used to validate given value against
    :type component: _PipelineComponent
    :param inputs: Inputs to the pipeline job.
    :type inputs: dict[str, Union[Input, str, bool, int, float]]
    :param outputs: Outputs the pipeline job.
    :type outputs: dict[str, Output]
    :param name: Name of the PipelineJob.
    :type name: str
    :param description: Description of the pipeline job.
    :type description: str
    :param display_name: Display name of the pipeline job.
    :type display_name: str
    :param experiment_name: Name of the experiment the job will be created under, if None is provided, experiment will be set to current directory.
    :type experiment_name: str
    :param jobs: Pipeline component node name to component object.
    :type jobs: dict[str, BaseNode]
    :param settings: Setting of pipeline job.
    :type settings: ~azure.ai.ml.entities.PipelineJobSettings
    :param identity: Identity that training job will use while running on compute.
    :type identity: Union[ManagedIdentity, AmlToken, UserIdentity]
    :param compute: Compute target name of the built pipeline.
    :type compute: str
    :param tags: Tag dictionary. Tags can be added, removed, and updated.
    :type tags: dict[str, str]
    :param schedule: Schedule definition of job. If no schedule is provided, the job will run once immediately after it is submitted.
    :type schedule: Union[~azure.ai.ml.entities.CronSchedule, ~azure.ai.ml.entities.RecurrenceSchedule]
    :param kwargs: A dictionary of additional configuration parameters.
    :type kwargs: dict
    """

    def __init__(
        self,
        *,
        component: _PipelineComponent = None,
        inputs: Dict[str, Union[Input, str, bool, int, float]] = None,
        outputs: Dict[str, Output] = None,
        name: str = None,
        description: str = None,
        display_name: str = None,
        experiment_name: str = None,
        jobs: Dict[str, BaseNode] = None,
        settings: PipelineJobSettings = None,
        identity: Union[ManagedIdentity, AmlToken, UserIdentity] = None,
        compute: str = None,
        tags: Dict[str, str] = None,
        schedule: Union[CronSchedule, RecurrenceSchedule] = None,
        **kwargs,
    ):
        # initialize io
        inputs, outputs = inputs or {}, outputs or {}
        if isinstance(component, _PipelineComponent) and component._source == ComponentSource.DSL:
            self._inputs = self._build_inputs_dict(component.inputs, inputs)
            # Build the outputs from entity output definition
            self._outputs = self._build_outputs_dict(component.outputs, outputs)
        else:
            # Build inputs/outputs dict without meta when definition not available
            self._inputs = self._build_inputs_dict_without_meta(inputs)
            self._outputs = self._build_outputs_dict_without_meta(outputs)
        if component is None:
            component = _PipelineComponent(
                components={}, description=description, display_name=display_name, _source=ComponentSource.YAML
            )

        self.component = component
        if "type" not in kwargs.keys():
            kwargs["type"] = "pipeline"
        super(PipelineJob, self).__init__(
            name=name,
            description=description or component.description,
            tags=tags,
            display_name=display_name or component.display_name,
            experiment_name=experiment_name,
            compute=compute,
            **kwargs,
        )

        self.jobs: Dict[str, BaseNode] = dict(jobs) if jobs else {}

        # remove swept Command
        node_names_to_skip = []
        for node_name, job_instance in self.jobs.items():
            if isinstance(job_instance, Command) and job_instance._swept is True:
                node_names_to_skip.append(node_name)

        for key in node_names_to_skip:
            del self.jobs[key]

        # TODO: check if we can merge validation logic to self._validate()
        for _, job_instance in self.jobs.items():
            if isinstance(job_instance, (Command, Sweep, Parallel)):
                job_instance._validate_inputs()
                binding_inputs = job_instance._build_inputs()
                if isinstance(job_instance.component, Component):
                    self._validate_pipeline_input(binding_inputs, job_instance.component.inputs)
            elif isinstance(job_instance, AutoMLJob):
                pass
            else:
                msg = f"Not supported pipeline job type: {type(job_instance)}"
                raise ValidationException(
                    message=msg,
                    no_personal_data_message=msg,
                    target=ErrorTarget.PIPELINE,
                    error_category=ErrorCategory.USER_ERROR,
                )
        self._remove_pipeline_input()
        self.compute = compute
        self._settings = settings if settings else PipelineJobSettings()
        self.identity = identity
        self._schedule = schedule
        # TODO: remove default code & environment?
        self._default_code = None
        self._default_environment = None

    @property
    def inputs(self) -> InputsAttrDict:
        """Inputs of the pipeline job.

        :return: Inputs of the pipeline job.
        :rtype: dict
        """
        return self._inputs

    @property
    def outputs(self) -> OutputsAttrDict:
        """Outputs of the pipeline job.

        :return: Outputs of the pipeline job.
        :rtype: dict
        """
        return self._outputs

    @property
    def schedule(self) -> Optional[Union[CronSchedule, RecurrenceSchedule]]:
        """Schedule of the pipeline job.

        :return: Schedule of the pipeline job.
        :rtype: Optional[Union[~azure.ai.ml.entities.CronSchedule, ~azure.ai.ml.entities.RecurrenceSchedule]]
        """
        return self._schedule

    @schedule.setter
    def schedule(self, value):
        self._schedule = value

    @property
    def settings(self) -> PipelineJobSettings:
        """Settings of the pipeline job.

        :return: Settings of the pipeline job.
        :rtype: ~azure.ai.ml.entities.PipelineJobSettings
        """
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = value

    def _validate(self, raise_error: bool = False) -> None:
        """Validate that all provided inputs and parameters are valid for current pipeline and components in it."""
        # TODO: validate before submit
        for node_name, node in self.jobs.items():
            if isinstance(node, (Command, Sweep, Parallel)):
                node._validate(raise_error=raise_error)
            elif isinstance(node, AutoMLJob):
                pass
            else:
                msg = f"Not supported pipeline job type: {type(node)}"
                raise ValidationException(
                    message=msg,
                    no_personal_data_message=msg,
                    target=ErrorTarget.PIPELINE,
                    error_category=ErrorCategory.USER_ERROR,
                )

    def _remove_pipeline_input(self):
        """Remove None pipeline input.If not remove, it will pass "None" to backend."""
        redundant_pipeline_inputs = []
        for pipeline_input_name, pipeline_input in self._inputs.items():
            if pipeline_input._data is None:
                redundant_pipeline_inputs.append(pipeline_input_name)
        for redundant_pipeline_input in redundant_pipeline_inputs:
            self._inputs.pop(redundant_pipeline_input)

    def _validate_pipeline_input(self, binding_inputs, component_definition_inputs):
        """Validate pipeline inputs is None or not. If it's None and used in input binding, raise error when
        it's binding component input is required and remove it when optional. If it's None and not used in input
        binding, remove it directly."""
        for component_input_name, component_binding_input in binding_inputs.items():
            if isinstance(component_binding_input, Input):
                component_binding_input = component_binding_input.path
            if is_data_binding_expression(component_binding_input):
                # todo: refine get pipeline_input_name from binding
                pipeline_input_name = component_binding_input[3:-2].split(".")[-1]
                if pipeline_input_name in self._inputs and self._inputs[pipeline_input_name]._data is None:
                    if component_definition_inputs[component_input_name]._optional:
                        # todo: not remove component input in client side, backend need remove component job
                        #  optional input which is binding to a None pipeline input
                        pass
                    else:
                        msg = "Pipeline input {} is None, but it's binding to a required component input {}, please set reasonable value."
                        raise UserErrorException(
                            message=msg.format(pipeline_input_name, component_input_name),
                            no_personal_data_message=msg.format("[pipeline_input_name]", "[component_input_name]"),
                        )

    def _check_private_preview_features(self):
        """Checks is private preview features included in pipeline.
        If private preview environment not set, raise exception.
        """
        if not is_private_preview_enabled():
            error_msg = (
                "{} is a private preview feature, "
                f"please set environment variable {AZUREML_PRIVATE_FEATURES_ENV_VAR} to true to use it."
            )
            # check has not supported nodes
            for _, node in self.jobs.items():
                if isinstance(node, Parallel):
                    msg = error_msg.format("Parallel job in pipeline")
                    raise UserErrorException(message=msg, no_personal_data_message=msg)
                if isinstance(node, AutoMLJob):
                    msg = error_msg.format("AutoML job in pipeline")
                    raise UserErrorException(message=msg, no_personal_data_message=msg)
            # check has not supported properties
            if self.schedule:
                msg = error_msg.format("Schedule")
                raise UserErrorException(message=msg, no_personal_data_message=msg)

    def _to_rest_object(self) -> JobBaseData:
        """Build current parameterized pipeline instance to a pipeline job object before submission.

        :return: Rest pipeline job.
        """
        # Check if there are private preview features in it
        self._check_private_preview_features()

        # Build the inputs to dict. Handle both value & binding assignment.
        # Example: {
        #   "input_data": {"data": {"path": "path/to/input/data"},  "mode"="Mount"},
        #   "input_value": 10,
        #   "learning_rate": "${{jobs.step1.inputs.learning_rate}}"
        # }
        built_inputs = self._build_inputs()

        # Build the outputs to dict
        # example: {"eval_output": "${{jobs.eval.outputs.eval_output}}"}
        built_outputs = self._build_outputs()

        self._validate()

        settings_dict = vars(self.settings) if self.settings else {}
        settings_dict = {key: val for key, val in settings_dict.items() if val is not None}

        # Build the jobs to dict
        rest_component_jobs = {}
        for job_name, job in self.jobs.items():
            if isinstance(job, BaseNode):
                rest_node_dict = job._to_rest_object()
            elif isinstance(job, AutoMLJob):
                rest_node_dict = json.loads(json.dumps(job._to_dict(inside_pipeline=True)))
                # TODO(1757200): remove this
                rest_node_dict.update(
                    {"properties": {"_automl_internal_label": "latest", "_automl_internal_save_mlflow": "true"}}
                )
            else:
                msg = f"Non supported job type in Pipeline jobs: {type(job)}"
                raise ValidationException(
                    message=msg,
                    no_personal_data_message=msg,
                    target=ErrorTarget.PIPELINE,
                    error_category=ErrorCategory.USER_ERROR,
                )
            rest_component_jobs[job_name] = rest_node_dict

        # TODO: Revisit this logic when multiple types of component jobs are supported
        rest_compute = self.compute

        pipeline_job = RestPipelineJob(
            compute_id=rest_compute,
            display_name=self.display_name,
            tags=self.tags,
            description=self.description,
            properties=self.properties,
            experiment_name=self.experiment_name,
            jobs=rest_component_jobs,
            inputs=to_rest_dataset_literal_inputs(built_inputs),
            outputs=to_rest_data_outputs(built_outputs),
            settings=settings_dict,
            identity=self.identity,
            schedule=self.schedule,
        )
        rest_job = JobBaseData(properties=pipeline_job)
        rest_job.name = self.name
        return rest_job

    @classmethod
    def _load_from_rest(cls, obj: JobBaseData) -> "PipelineJob":
        properties: RestPipelineJob = obj.properties
        # Workaround for BatchEndpoint as these fields are not filled in
        # Unpack the inputs
        from_rest_inputs = from_rest_inputs_to_dataset_literal(properties.inputs) or {}
        from_rest_outputs = from_rest_data_outputs(properties.outputs) or {}
        # Unpack the component jobs
        if properties.jobs:
            sub_nodes = {}
            for node_name, node in properties.jobs.items():
                if "type" in node and node["type"] == NodeType.SWEEP:
                    sub_nodes[node_name] = Sweep._from_rest_object(node)
                elif "type" in node and node["type"] == NodeType.AUTOML:
                    # rest dict outputs -> Output objects
                    outputs = AutoMLJob._from_rest_outputs(node.get("outputs"))
                    # Output objects -> yaml dict outputs
                    parsed_outputs = {}
                    for key, val in outputs.items():
                        if isinstance(val, Output):
                            val = val._to_dict()
                        parsed_outputs[key] = val
                    node["outputs"] = parsed_outputs
                    sub_nodes[node_name] = AutoMLJob._load_from_dict(
                        node,
                        context={BASE_PATH_CONTEXT_KEY: "./"},
                        additional_message="Failed to load automl task from backend.",
                        inside_pipeline=True,
                    )
                elif "type" in node and node["type"] == NodeType.PARALLEL:
                    sub_nodes[node_name] = Parallel._from_rest_object(node)
                else:
                    sub_nodes[node_name] = Command._from_rest_object(node)
        else:
            sub_nodes = None
        # backend may still store Camel settings, eg: DefaultDatastore, translate them to snake when load back
        settings_dict = transform_dict_keys(properties.settings, camel_to_snake) if properties.settings else None
        settings_sdk = PipelineJobSettings(**settings_dict) if settings_dict else PipelineJobSettings()
        job = PipelineJob(
            component=_PipelineComponent._load_from_rest_pipeline_job(
                dict(
                    inputs=from_rest_inputs,
                    outputs=from_rest_outputs,
                    display_name=properties.display_name,
                    description=properties.description,
                )
            ),
            inputs=from_rest_inputs,
            outputs=from_rest_outputs,
            name=obj.name,
            id=obj.id,
            display_name=properties.display_name,
            tags=properties.tags,
            properties=properties.properties,
            experiment_name=properties.experiment_name,
            status=properties.status,
            creation_context=obj.system_data,
            services=properties.services,
            compute=properties.compute_id,
            jobs=sub_nodes,
            settings=settings_sdk,
            identity=properties.identity,
            schedule=Schedule._from_rest_object(properties.schedule) if properties.schedule else None,
        )

        return job

    def _to_dict(self) -> Dict:
        return PipelineJobSchema(context={BASE_PATH_CONTEXT_KEY: "./"}).dump(self)

    @classmethod
    def _component_items_from_path(cls, data: Dict):
        if "jobs" in data:
            for node_name, job_instance in data["jobs"].items():
                potential_component_path = job_instance["component"] if "component" in job_instance else None
                if isinstance(potential_component_path, str) and potential_component_path.startswith("file:"):
                    yield node_name, potential_component_path

    @classmethod
    def _load_from_dict(cls, data: Dict, context: Dict, additional_message: str, **kwargs) -> "PipelineJob":
        path_first_occurrence = {}
        component_first_occurrence = {}
        for node_name, component_path in cls._component_items_from_path(data):
            if component_path in path_first_occurrence:
                component_first_occurrence[node_name] = path_first_occurrence[component_path]
                # set components to be replaced here may break the validation logic
            else:
                path_first_occurrence[component_path] = node_name

        loaded_schema = load_from_dict(PipelineJobSchema, data, context, additional_message, **kwargs)

        # replace repeat component with first occurrence to reduce arm id resolution
        # current load yaml file logic is in azure.ai.ml._schema.core.schema.YamlFileSchema.load_from_file
        # is it possible to load the same yaml file only once in 1 pipeline loading?
        for node_name, first_occurrence in component_first_occurrence.items():
            job = loaded_schema["jobs"][node_name]
            job._component = loaded_schema["jobs"][first_occurrence].component
            # For Parallel job, should also align task attribute which is usually from component.task
            if isinstance(job, Parallel):
                job.task = loaded_schema["jobs"][first_occurrence].task
        return PipelineJob(base_path=context[BASE_PATH_CONTEXT_KEY], **loaded_schema)

    def __str__(self):
        try:
            return self._ordered_yaml()
        except BaseException:
            return super(PipelineJob, self).__str__()

    def _get_telemetry_values(self):
        telemetry_values = super()._get_telemetry_values()
        telemetry_values.update(
            {
                "source": self.component._source.value,
                "node_count": len(self.jobs),
            }
        )
        return telemetry_values

    def _to_component(self, pipeline_job_inputs: Dict, context):
        msg = "Translating a PipelineJob to a component is not supported."
        raise ValidationException(
            message=msg,
            no_personal_data_message=msg,
            target=ErrorTarget.PIPELINE,
            error_category=ErrorCategory.USER_ERROR,
        )
