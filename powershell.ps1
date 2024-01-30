Connect-AzAccount -TenantId 0101e75a-c84d-4507-9bba-6634e25b3f82
Select-AzSubscription -SubscriptionName sp-pl-datafactory-nonprod-000  
Get-AzDataFactoryV2Trigger -ResourceGroupName "rg_spark-good-data-factory_westus2_w06" -DataFactoryName "adfspark-good-data-factoryw06"
