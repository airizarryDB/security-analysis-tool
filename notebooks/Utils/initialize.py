# Databricks notebook source
# MAGIC %run ./common

# COMMAND ----------

#replace values for accounts exec
hostname = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().getOrElse(None)
cloud_type = getCloudType(hostname)

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Modify JSON values
# MAGIC * **account_id** Account ID. Can get this from the accounts console
# MAGIC * **sql_warehouse_id** SQL Warehouse ID to import dashboard
# MAGIC * **username_for_alerts** A valid Databricks username to receive alerts 
# MAGIC * **verbosity** (optional). debug, info, warning, error, critical
# MAGIC * **master_name_scope** Secret Scope for Account Name
# MAGIC * **master_name_key** Secret Key for Account Name
# MAGIC * **master_pwd_scope** Secret Scope for Account Password
# MAGIC * **master_pwd_key** Secret Key for Account Password
# MAGIC * **workspace_pat_scope** Secret Scope for Workspace PAT
# MAGIC * **workspace_pat_token_prefix** Secret Key prefix for Workspace PAT. Workspace ID will automatically be appended to this per workspace
# MAGIC * **use_mastercreds** (optional) Use master account credentials for all workspaces

# COMMAND ----------

import json

json_ = {
   "account_id":"",
   "sql_warehouse_id":"",
   "username_for_alerts":"",
   "verbosity":"info"
}

# COMMAND ----------

json_.update({
   "master_name_scope":"sat_scope",
   "master_name_key":"user",
   "master_pwd_scope":"sat_scope",
   "master_pwd_key":"pass",
   "workspace_pat_scope":"sat_scope",
   "workspace_pat_token_prefix":"sat-token",
   "dashboard_id":"317f4809-8d9d-4956-a79a-6eee51412217",
   "dashboard_folder":"../../dashboards/",
   "dashboard_tag":"SAT",
   "use_mastercreds":True
})


# COMMAND ----------

# DBTITLE 1,GCP configurations 
if cloud_type == 'gcp':
    json_.update({
       "service_account_key_file_path":"/dbfs/FileStore/tables/SA_1_key.json",
       "impersonate_service_account":"arun-sa-2@fe-dev-sandbox.iam.gserviceaccount.com",
       "generate_pat_tokens":False,
       "use_mastercreds":False
    })


# COMMAND ----------

# DBTITLE 1,Azure configurations 
if cloud_type == 'azure':
    json_.update({
       "account_id":"azure", 
       "subscription_id":"3f2e4d32-8e8d-46d6-82bc-5bb8d962328b", # Azure subscriptionId
       "tenant_id":"9f37a392-f0ae-4280-9796-f1864a10effc", #The Directory (tenant) ID for the application registered in Azure AD.
       "client_id":"e06da8c0-f548-4a1a-bb68-6eaa3b26babc", # The Application (client) ID for the application registered in Azure AD.
       "client_secret":dbutils.secrets.get(json_['master_name_scope'], 'client_secret')  #The secret generated by AAD during your confidential app registration
     })

