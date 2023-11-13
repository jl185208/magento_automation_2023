Feature: Woocom Article Sync

  Scenario: Validate article creation in Woocom
     When that article is added in woocom
     Then article should be in woocom ocs
     #And article should be in article endpoint
     And article should be in woocom dynamodb
     And OCS-T16XX should be updated to Zephyr