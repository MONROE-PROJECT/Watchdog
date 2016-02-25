# Watchdog
The system self-test and repair for the MONROE node.

## Running 

    > biteback -R -F 

runs the biteback tests, but does not execute repair actions or final actions

    > biteback
    
runs the biteback tests. If a test fails, the repair actions are executed in order. 
After each repair action, the original test is repeated until the test succeeds, or 
there are no more repair actions left. 

If the test still fails after all repair actions are exhausted, the final action is 
executed.

## Extending

Biteback is a modular system. To extend it, just add a new file into the modules/ folder. 
It should extend the module class, and add itself to the registry using the register.put() method.

Please examine the exsting tests for examples. 

Think of biteback as a somewhat upgraded shell script. The util module contains some helper methods 
to quickly execute shell commands and monitor the results.
