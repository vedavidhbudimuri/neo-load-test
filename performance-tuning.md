Neo4j Memory Management:
We should configure types of memory for memory

```yaml
page_cache:
  description: Used to cache neo4j indexes and data
  config_parameters:
    - dbms.memory.pagecache.size

heap_size:
  description:
    Used for query execution, transaction state, management of the graph
    etc.
  config_parameters:
    - dbms.memory.heap.initial_size
    - dbms.memory.heap.max_size
  recommendations:
    - To set these two parameters to the same value. This will help avoid unwanted full garbage collection pauses.

os_memory:
  description: Reserved for OS
	min: 1GB
  how_to_get_value: will be allocated after heap_size and page_cache are allocated
  warning:
  - Cannot be explicitly configured

lucene_index_cache:
  description: For internal index
  how_to_get_value: will be allocated after heap_size and page_cache are allocated
  warning:
  - Cannot be explicitly configured


transaction_state:
  description:
    the memory that is needed to hold data and intermediate results in
    transactions that update records in the database.
  config_parameters:
    - dbms.tx_state.memory_allocation
    - dbms.tx_state.max_off_heap_memory
  recommendations:
    - Keeping transaction state off-heap is particularly beneficial to applications characterized by large, write-intensive transactions.
```

Considerations:

- Always use explicity configuration
- Initial memory recommendation (`neo4j-admin memrec`)
- Inspect the memory settings of a database (`neo4j-admin memrec --database`)

Capacity Planning

- `dbms.memory.pagecache.size=Total size(index + data) * some growth factor`

Index Configuration

- Use native provider

* native B+Tree Limitations

  -

```cypher
create index on :Post(title);
create index on :Post(createdAt);
create index on :Post(score);
create index on :Post(views);
create index on :Post(favorites);
create index on :Post(answers);
create index on :Post(score);

create index on :User(name);
create index on :User(createdAt);
create index on :User(reputation);
create index on :User(age);

create index on :Tag(count);

create constraint on (t:Tag) assert t.tagId is unique;
create constraint on (u:User) assert u.userId is unique;
create constraint on (p:Post) assert p.postId is unique;




CALL apoc.periodic.iterate(
'CALL apoc.load.csv(\'posts.csv\') YIELD lineNo, map as row, list return row',
'MERGE (post: Post {id:row.`postId:ID(Post)`}) ON CREATE SET post.title = row.title, post.body = row.body, post.score = row.score, post.views = row.views, post.comments = row.comments;',
{batchSize:10000, iterateList:true, parallel:true}
)


CALL apoc.periodic.iterate(
'CALL apoc.load.csv(\'users.csv\') YIELD lineNo, map as row, list return row',
'MERGE (owner:User {id:row.`userId:ID(User)`})
ON CREATE SET owner.displayname = row.displayname,
owner.reputation = row.reputation,
owner.aboutme = row.aboutme,
owner.websiteurl = row.websiteurl,
owner.location = row.location,
owner.profileimageurl = row.profileimageurl,
owner.views = row.views,
owner.upvotes = row.upvotes,
owner.downvotes = row.downvotes;',
{batchSize:10000, iterateList:true, parallel:true}
)


CALL apoc.periodic.iterate(
'CALL apoc.load.csv(\'tags.csv\') YIELD lineNo, map as row, list return row',
'MERGE (tag: Tag {id:row.`tagId:ID(Tag)`})',
{batchSize:10000, iterateList:true, parallel:true}
)


CALL apoc.periodic.iterate(
'CALL apoc.load.csv(\'tags_ports_rel.csv\') YIELD lineNo, map as row, list return row',
'MATCH (tag:Tag {id:apoc.convert.toString(row.`:END_ID(Tag)`)})
MATCH (post:Post {id:apoc.convert.toString(row.`:START_ID(Post)`)})
MERGE (post)-[:TAGGED]->(tag);',
{batchSize:10000, iterateList:true, parallel:true}
)


CALL apoc.periodic.iterate(
'CALL apoc.load.csv(\'posts_rel.csv\') YIELD lineNo, map as row, list return row',
'MATCH (child_post:Post {id:apoc.convert.toString(row.`:END_ID(Post)`)})
MATCH (parent_post:Post {id:apoc.convert.toString(row.`:START_ID(Post)`)})
MERGE (parent_post)-[:PARENT_OF]->(child_post);',
{batchSize:10000, iterateList:true, parallel:true}
)


CALL apoc.periodic.iterate(
'CALL apoc.load.csv(\'user_posts_rel.csv\') YIELD lineNo, map as row, list return row',
'MATCH (post:Post {id:apoc.convert.toString(row.`:END_ID(Post)`)})
MATCH (owner:User {id:apoc.convert.toString(row.`:START_ID(User)`)})
MERGE (owner)-[:ASKED]->(post);',
{batchSize:10000, iterateList:true, parallel:true}
)

```
