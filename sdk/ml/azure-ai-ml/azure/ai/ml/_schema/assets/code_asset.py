# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
import uuid

from azure.ai.ml._schema.core.fields import ArmStr

from .asset import AnonymousAssetSchema
from .artifact import ArtifactSchema
from azure.ai.ml.constants import BASE_PATH_CONTEXT_KEY, AzureMLResourceType
from marshmallow import ValidationError, fields, post_load, pre_dump

module_logger = logging.getLogger(__name__)


class CodeAssetSchema(ArtifactSchema):
    id = ArmStr(azureml_type=AzureMLResourceType.CODE, dump_only=True)
    path = fields.Str(
        metadata={
            "description": "A local path or a Blob URI pointing to a file or directory where code asset is located."
        }
    )

    @post_load
    def make(self, data, **kwargs):
        from azure.ai.ml.entities._assets import Code

        return Code(**data)


class AnonymousCodeAssetSchema(CodeAssetSchema, AnonymousAssetSchema):
    @post_load
    def make(self, data, **kwargs):
        from azure.ai.ml.entities._assets import Code

        return Code(
            name=str(uuid.uuid4()),
            version="1",
            is_anonymous=True,
            base_path=self.context[BASE_PATH_CONTEXT_KEY],
            **data
        )

    @pre_dump
    def validate(self, data, **kwargs):
        # AnonymousCodeAssetSchema does not support None or arm string(fall back to ArmVersionedStr)
        if data is None or not hasattr(data, "get"):
            raise ValidationError("Code cannot be None")
        return data
