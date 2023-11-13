Feature: Magento Article Sync

  Scenario: Validate article creation in Magento
     When that article is added in magento
     Then article should be in ocs
     And article should be in article endpoint
     And article should be in dynamodb
     And OCS-T1633 should be updated to Zephyr
