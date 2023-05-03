# ibm-instana-ansible

The IBM Instana collection provides the ability for Instana event data to be consumed by Event Driven Ansible (EDA). In EDA, rulebooks are defined with 'If-This-Then-That' conditions. The condition uses parsed Instana event data to trigger automation. This enables you to build existing operational knowledge into automated decision-making and actions, so that you can efficiently perform repetitive tasks and deliver services faster, with far less effort while reducing Mean-Time-To-Resolution (MTTR).

## Prequisite 

```
    ansible-galaxy collection install ansible.eda
```

## Using the collection

```
    Install the collection: ansible-galaxy collection install ibm.instana
```    
    Once installed, define the instana_webhook in the source of the rulebook.
    Then, define rules with conditions based on the event payload coming from Instana.
    
        - name: Listen for events on a webhook
          hosts: all
        
          ## Define our source for events
        
          sources:
           - instana_webhook:
               host: 0.0.0.0
               port: 5000
        
         ## Define the conditions we are looking for
        
          rules:
           - name: Test
             condition: event.payload.message == "Node failed"
             action:
                run_playbook:
                  name: launch_controller_job.yml
           - name: Event
             condition: event.payload.problem.problemText == "Erroneous call rate is too high"
             action:
                run_playbook:
                  name: launch_controller_job.yml
                  
    
    
    Now, in Instana use the action framework to create an action which will invoke the rulebook webhook above, and 
    pass in the event payload to trigger the condition defined in the rulebook.
    
    Here is an action example:
    
    # The @@eda_server@@ is parameter which points to the webhook host and port above.
    # The ${INSTANA_EVENT} is the content of event associated to the action below. 
    
    #!/bin/bash

    # Verify Instana event metadata exists
    if [ -z "${INSTANA_EVENT}" ]; then
      # Action running in test mode
      curl -H 'Content-Type: application/json' -d "{\"message\": \"Node failed\"}" @@eda_server@@/instana
    else
      # Action run from event
      curl -H 'Content-Type: application/json' -d "${INSTANA_EVENT}" @@eda_server@@/instana
    fi
  


## Requirements

```
    anisble >= =2.9.10
    python  >= 3.9 
```

## Licensing

[Apache-2.0](http://www.apache.org/licenses/LICENSE-2.0)  


## Release Notes

[Please see the change log](https://github.com/instana/ibm-instana-ansible/blob/main/CHANGELOG.rst)
