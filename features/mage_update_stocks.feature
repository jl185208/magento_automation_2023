Feature: Magento Sales Order Mapper

  Scenario: Validate Sales Order Mapper Magento
     #When that article is added in magento
     #Then article should be in ocs
     When article should be in stockitems endpoint
     And article should be in dynamodb
     When stocks is updated in eventbridge
     Then stocks should be in skustockitems endpoint
     And OCS-T1651 should be updated to Zephyr
     