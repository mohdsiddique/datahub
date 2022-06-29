import datahub.emitter.mce_builder as builder
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import (
    ChangeTypeClass,
    CorpGroupInfoClass,
    CorpRoleInfoClass,
    CorpUserInfoClass,
    DataPolicyInfoClass,
    DataPolicyTypeClass,
    DatasetPropertiesClass,
    InheritedRoleClass,
    ResourceIdentifierTypeClass,
    ResourceKeywordClass,
    ResourcePrincipalPolicyClass,
    ResourceReferenceClass,
    RoleMembershipClass,
)

corp_role_info = CorpRoleInfoClass(displayName="analyst")
corp_role_urn = builder.make_role_urn("analyst")

corp_role_soap_analyst_info = CorpRoleInfoClass(displayName="soap_analyst")
corp_role_soap_analyst_urn = builder.make_role_urn("soap_analyst")
corp_parent_role = InheritedRoleClass(roles=[corp_role_urn])

corp_user_info1 = CorpUserInfoClass(displayName="John", active=True)
corp_user_1_urn = builder.make_user_urn("john@acryldata.io")

corp_user_info2 = CorpUserInfoClass(displayName="David", active=True)
corp_user_2_urn = builder.make_user_urn("david@acryldata.io")

dataset_info = DatasetPropertiesClass(description="sales dataset")
dataset_urn = builder.make_dataset_urn("postgres", "db.public.sale")

corp_group_info = CorpGroupInfoClass(
    displayName="sales representatives",
    admins=[corp_user_1_urn],
    members=[corp_user_2_urn],
    groups=[],
)
corp_group_urn = builder.make_group_urn("sales_representative")


resource_reference = ResourceReferenceClass(
    type=ResourceIdentifierTypeClass.RESOURCE_URN,
    resourceUrn=dataset_urn,
)

resource_principal_policy = ResourcePrincipalPolicyClass(
    principal=builder.make_role_urn("analyst"),
    resourceRef=resource_reference,
    permission="SELECT",
    isAllow=True,
)

data_policy_info_class = DataPolicyInfoClass(
    type=DataPolicyTypeClass.ResourcePrincipalPolicy,
    resourcePrincipalPolicy=resource_principal_policy,
    displayName="Dataset {} access policy".format("sale"),
)
data_policy_urn = builder.make_data_policy_urn(
    platform="redshift", name="db.public.sale#analyst#SELECT"
)

role_membership = RoleMembershipClass(roles=[corp_role_urn])

# Construct a MetadataChangeProposalWrapper object.
corp_role_mcp = MetadataChangeProposalWrapper(
    entityType="corpRole",
    changeType=ChangeTypeClass.UPSERT,
    entityUrn=corp_role_urn,
    aspectName="corpRoleInfo",
    aspect=corp_role_info,
)

corp_role_soap_analyst_mcp = MetadataChangeProposalWrapper(
    entityType="corpRole",
    changeType=ChangeTypeClass.UPSERT,
    entityUrn=corp_role_soap_analyst_urn,
    aspectName="corpRoleInfo",
    aspect=corp_role_soap_analyst_info,
)

corp_role_parent_mcp = MetadataChangeProposalWrapper(
    entityType="corpRole",
    changeType=ChangeTypeClass.UPSERT,
    entityUrn=corp_role_soap_analyst_urn,
    aspectName="inheritedRole",
    aspect=corp_parent_role,
)


corp_user_info1_mcp = MetadataChangeProposalWrapper(
    entityType="corpUser",
    changeType=ChangeTypeClass.UPSERT,
    entityUrn=corp_user_1_urn,
    aspectName="corpUserInfo",
    aspect=corp_user_info1,
)

corp_user_info2_mcp = MetadataChangeProposalWrapper(
    entityType="corpUser",
    changeType=ChangeTypeClass.UPSERT,
    entityUrn=corp_user_2_urn,
    aspectName="corpUserInfo",
    aspect=corp_user_info2,
)

corp_user_1_rm_mcp = MetadataChangeProposalWrapper(
    entityType="corpUser",
    changeType=ChangeTypeClass.UPSERT,
    entityUrn=corp_user_1_urn,
    aspectName="roleMembership",
    aspect=role_membership,
)

corp_user_2_rm_mcp = MetadataChangeProposalWrapper(
    entityType="corpUser",
    changeType=ChangeTypeClass.UPSERT,
    entityUrn=corp_user_2_urn,
    aspectName="roleMembership",
    aspect=role_membership,
)

corp_group_info_mcp = MetadataChangeProposalWrapper(
    entityType="corpGroup",
    changeType=ChangeTypeClass.UPSERT,
    entityUrn=corp_group_urn,
    aspectName="corpGroupInfo",
    aspect=corp_group_info,
)

corp_group_rm_mcp = MetadataChangeProposalWrapper(
    entityType="corpGroup",
    changeType=ChangeTypeClass.UPSERT,
    entityUrn=corp_group_urn,
    aspectName="roleMembership",
    aspect=role_membership,
)

corp_data_policy_mcp = MetadataChangeProposalWrapper(
    entityType="dataPolicy",
    changeType=ChangeTypeClass.UPSERT,
    entityUrn=data_policy_urn,
    aspectName="dataPolicyInfo",
    aspect=data_policy_info_class,
)

dataset_mcp = MetadataChangeProposalWrapper(
    entityType="dataset",
    changeType=ChangeTypeClass.UPSERT,
    entityUrn=dataset_urn,
    aspectName="datasetProperties",
    aspect=dataset_info,
)

# Samples data-policy for Special Resource "ALL"

resource_reference_all = ResourceReferenceClass(
    type=ResourceIdentifierTypeClass.SPECIAL,
    special=ResourceKeywordClass.ALL,
)

resource_principal_policy_all = ResourcePrincipalPolicyClass(
    principal=builder.make_role_urn("analyst"),
    resourceRef=resource_reference_all,
    permission="UPDATE",
    isAllow=True,
)

data_policy_info_class_all = DataPolicyInfoClass(
    type=DataPolicyTypeClass.ResourcePrincipalPolicy,
    resourcePrincipalPolicy=resource_principal_policy_all,
    displayName="Update on ALL resources",
)
data_policy_urn_all = builder.make_data_policy_urn(
    platform="redshift", name="db.public.sale#analyst#UPDATE"
)

corp_data_policy_mcp_all = MetadataChangeProposalWrapper(
    entityType="dataPolicy",
    changeType=ChangeTypeClass.UPSERT,
    entityUrn=data_policy_urn_all,
    aspectName="dataPolicyInfo",
    aspect=data_policy_info_class_all,
)
# Create an emitter to the GMS REST API.
emitter = DatahubRestEmitter("http://localhost:8080")

mcps = [
    dataset_mcp,
    corp_role_mcp,
    corp_user_info1_mcp,
    corp_user_info2_mcp,
    corp_group_info_mcp,
    corp_user_1_rm_mcp,
    corp_user_2_rm_mcp,
    corp_group_rm_mcp,
    corp_data_policy_mcp,
    corp_data_policy_mcp_all,
    corp_role_soap_analyst_mcp,
    corp_role_parent_mcp,
]

for mcp in mcps:
    emitter.emit_mcp(mcp)