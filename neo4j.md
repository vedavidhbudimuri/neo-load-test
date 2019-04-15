Neo4j Exploration

- [x] Currently trying to install Neo4j Docker in an ec2 install. Next step would be to write a python snippet for load test
  1. Checklist
     - [x] Should be able to connect and access to Neo4j
- [x] Shutdown ec2 server
- [x] Find the proper sdk to write the script
  1. Finalized on Py2neo
- [ ] PoC for features related to Neo4j

  - [ ] Should be able to view the nodes along with the information
  - [ ] Communication properties of the relation between the nodes
  - [ ] Node Analysis
    - [ ] Just showing the nodes
  - [ ] Frequent Communication Analysis
    - [ ] Changing the color of the relation depending on how frequent they have communicated (by keeping track of the number of times they have communicated)
  - [ ] Internal Communication Analysis
    - [ ] Louvain Modularity
  - [ ] Symmetric and Structured Layout
    - [ ] What do they mean by symmetric and structured layout
    - [ ] Here they simply want to us to high light the nodes which have more connections (we can have a gradient depending on the number of connections a node has (while keeping track of the number of communications a node has made))
  - [ ] Isolated Communication
    - [ ] How come there be any one which doesn’t have any connection as we are adding things into database only whenever there is communication between two nodes
  - [ ] Map Support
  - [ ] Other Presentation Requirements

    - [ ] What do they mean by text comment
    - [ ] Should be able to node properties
    - [ ] Searching the graph
    - [ ] Ignore a particular node -> should this be effecting the behavior of the above analysis
    - [ ] Deleting the nodes

  - Questions
    - What do they mean by reconstruct? (Link Chart Analysis)
    - Node Analysis
      - What do they mean by highlighting communication patterns?
    -

* [ ] Check how to write load test script
  - [ ] Need to get all the use cases
    - [ ] Single read
    - [ ] Single write
    - [ ] Bulk read
    - [ ] Bulk write
    - [ ] Concurrency
    - [ ] Properties
    - [ ] Graph Algorithms
    - [ ]

1. Need to check with the best practices for the tuning
2. Tuning Neo4j for better performance
3.

Things Im not clear of

1. Can we create multiple relation ships between two nodes (We can)
2. Counter intuitive grouping in case of leaf nodes.
3. What other cases will be counter intuitive?
4. How do projections our grouping a sub graph work
5. Need to check if things work the same way in the case of multiple types of relations
6. Need to check if things work the same way in the case of multiple relations (yes it is)
