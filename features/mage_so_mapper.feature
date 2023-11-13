Feature: Magento Sales Order Mapper

  Scenario: Validate Sales Order Mapper Magento
     When sales order is created in magento
     Then sales order is in orders endpoint
     And invoice is sent in magento
     And sales order is in dynamodb
     When shipped status sent in events
     Then order endpoint status should be complete
     And sales order in magento should be Complete
     And OCS-T1641 should be updated to Zephyr