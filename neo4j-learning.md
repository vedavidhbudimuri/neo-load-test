Neo4j Learning Notes

1. Community Edition
   1. For single Instance Deployment
   2. Supports
      1. ACID
      2. Cypher Support
   3. Ideal for
      1. Applications in small workgroups
   4. Limits
      1. 34B nodes, 34B relationships, 68B properties
2. Enterprise Edition

3. [System Requirements](https://neo4j.com/docs/operations-manual/3.5/installation/requirements/)

   1. CPU:

      `Minimum: Intel Core i3`

      `Recommended: Intel Core i7 IBM POWER8`

   2. Memory

      `Minimum: 2 GB`

      `Recommended: 16GB or more`

   - [Memory Configuration](https://neo4j.com/docs/operations-manual/3.5/performance/memory-configuration/)
     - Types of Memory Used:
       - OS Memory
       - Lucene Index
       - Page Cache
         `dbms.memory.pagecache.size`
       - Heap size
         `dbms.memory.heap.initial_size`
         `dbms.memory.heap.max_size`
         - Suggested to set the above two to same value to avoid unwanted garbage collection pauses
       - Transaction state
         `dbms.tx_state.memory_allocation: heap or off-heap`
         `dbms.tx_state.max_off_heap_memory`
         - Keeping transaction state `off-heap` is particularly beneficial to applications characterized by large, write-intensive transactions
       - OS Memory, Lucene Index cannot be configured
     - Considerations
       - Always use explicit configuration
       - Initial memory recommendation
     -

   3. Storage

- Cypher Querying
  - WHERE (It should not be seen as a filter after the matching is finished.)
    - AND, OR, XOR, NOT
    - null
    - filtering on
      - labels
      - properties
      - dynamically computed properties
      - patterns
    - exists
    - string matching
      - starts with
      - ends with
      - regular expressions
    - IN
    - \>, <, >=, <=
  - Pagination
    - SKIP
    - LIMIT
  - Ordering
    - ORDER BY
  - MATCH
    - Variable length relationships
  - CALL
    - to call a procedure deployed in the database
  - YIELD
    - Using call results
  - WITH
    - The WITH clause allows query parts to be chained together, piping the results from one to be used as starting points or criteria in the next.
  - FOREACH
  - Indexes

1. Start with a Small Sample -> Nothing To Do
2. MERGE on a Key -> Single key in merge
3. Use Constraints and Indexes
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

4. Use Only One MERGE Statement
5. Use DISTINCT
6. Use PERIODIC COMMIT

LOAD CSV WITH HEADERS FROM "questions.csv" AS row
WITH row LIMIT 1000

CREATE CONSTRAINT ON (q:Question) ASSERT q.id IS UNIQUE
CREATE CONSTRAINT ON (u:User) ASSERT u.id IS UNIQUE
CREATE CONSTRAINT ON (a:Answer) ASSERT a.id IS UNIQUE

LOAD CSV WITH HEADERS FROM "" AS row
MERGE (question: Question {id:row.question_id}
ON CREATE SET question.title = row.title,
question.up_vote_count = row.up_vote_count,
question.creation_date = row.creation_date;

LOAD CSV WITH HEADERS FROM "" AS row
MERGE (owner:User {id:row.owner_user_id})
ON CREATE SET owner.display_name = row.owner_display_name;

LOAD CSV WITH HEADERS FROM "" AS row
MERGE (owner:Question {id:row.question_id})
MATCH (owner:User {id:row.owner_user_id})
MERGE (owner)-[:ASKED]->(question);

CREATE CONSTRAINT ON (q:Post) ASSERT q.id IS UNIQUE
CREATE CONSTRAINT ON (u:User) ASSERT u.id IS UNIQUE

WITH '' AS posts_file
CALL apoc.load.json(posts_file) YIELD value as row

MERGE (post: Post {id:row.`postId:ID(Post)`}
ON CREATE SET post.title = row.title,
post.body = row.body,
post.score = row.score,
post.views = row.views,
post.comments = row.comments;

MERGE (post: Post {id:row.`postId:ID(Post)`})
ON CREATE SET post.title = row.title,
post.body = row.body,
post.score = row.score,
post.views = row.views,
post.comments = row.comments;

WITH '' AS users_file
CALL apoc.load.json(users_file) YIELD value as row
MERGE (owner:User {id:row.`userId:ID(User)`})
ON CREATE SET owner.displayname = row.displayname,
owner.reputation = row.reputation,
owner.aboutme = row.aboutme,
owner.websiteurl = row.websiteurl,
owner.location = row.location,
owner.profileimageurl = row.profileimageurl,
owner.views = row.views,
owner.upvotes = row.upvotes,
owner.downvotes = row.downvotes;

---

CALL apoc.load.csv('/var/lib/neo4j/import/users.csv') YIELD lineNo, map as row, list

MERGE (owner:User {id:row.`userId:ID(User)`})
ON CREATE SET owner.displayname = row.displayname,
owner.reputation = row.reputation,
owner.aboutme = row.aboutme,
owner.websiteurl = row.websiteurl,
owner.location = row.location,
owner.profileimageurl = row.profileimageurl,
owner.views = row.views,
owner.upvotes = row.upvotes,
owner.downvotes = row.downvotes;

---

CALL apoc.periodic.iterate(
'CALL apoc.load.csv(\'/var/lib/neo4j/import/users.csv\') YIELD lineNo, map as row, list return row',
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
);

CALL apoc.periodic.iterate(
'CALL apoc.load.csv(\'/var/lib/neo4j/import/posts.csv\') YIELD lineNo, map as row, list return row',
'MERGE (post: Post {id:row.`postId:ID(Post)`})
ON CREATE SET post.title = row.title,
post.body = row.body,
post.score = row.score,
post.views = row.views,
post.comments = row.comments;',
{batchSize:10000, iterateList:true, parallel:true}
);

CALL apoc.periodic.iterate(
'CALL apoc.load.csv(\'/var/lib/neo4j/import/tags.csv\') YIELD lineNo, map as row, list return row',
'MERGE (tag: Tag {id:row.`tagId:ID(Tag)`})'
{batchSize:1000, iterateList:true, parallel:true}
);

CALL apoc.periodic.iterate(
'CALL apoc.load.csv(\'/var/lib/neo4j/import/tags_posts_rel.csv\') YIELD lineNo, map as row, list return row',
'MATCH (tag:Tag {id:apoc.convert.toString(row.`:END_ID(Tag)`)})
MATCH (post:Post {id:apoc.convert.toString(row.`:START_ID(Post)`)})
MERGE (post)-[:TAGGED]->(tag);',
{batchSize:1000, iterateList:true, parallel:false}
);

CALL apoc.periodic.iterate(
'CALL apoc.load.csv(\'/var/lib/neo4j/import/posts_rel.csv\') YIELD lineNo, map as row, list return row',
'MATCH (child_post:Post {id:apoc.convert.toString(row.`:END_ID(Post)`)})
MATCH (parent_post:Post {id:apoc.convert.toString(row.`:START_ID(Post)`)})
MERGE (parent_post)-[:PARENT_OF]->(child_post);',
{batchSize:1000, iterateList:true, parallel:false}
);

CALL apoc.periodic.iterate(
'CALL apoc.load.csv(\'/var/lib/neo4j/import/users_posts_rel.csv\') YIELD lineNo, map as row, list return row',
'MATCH (post:Post {id:apoc.convert.toString(row.`:END_ID(Post)`)})
MATCH (owner:User {id:apoc.convert.toString(row.`:START_ID(User)`)})
MERGE (owner)-[:ASKED]->(post);',
{batchSize:10000, iterateList:true, parallel:false}
);

---

4 Cores 16 GB RAM
9737248: Users:
page_cache:8
heap_init:8
heap_max:8

    500 -> 225
    1000 -> 225

16 Cores 64 GB RAM

9737248: Users:
page_cache:8
heap_init:12
heap_max:12

    10000 -> 128

    100000 -> 269

4,28,50,538: Posts:
10000 -> 483, 502

Relations:
10000 ->

Neo4j: 1) Data loading:
Approaches:
Common: 1) Creating constraints is more performant than normal 2)

        1) admin-load
            Can only be used on fresh database
        2) LOAD CSV
            4 Cores 16 GB RAM
                9737247:
                    10000 -> 441s
                        page_cache: 8GB
                        heap_init: 4GB
                        heap_max: 12GB

        3) Using APOC lib
            4 Cores 16 GB RAM
                9737247:
                    1000 -> 225s
                        page_cache: 8GB
                        heap_init: 8GB
                        heap_max: 8GB

                    100000 -> 223s
                        page_cache: 8GB
                        heap_init: 8GB
                        heap_max: 8GB

            After this we were unable to start the server (it was taking too long time) so migrated to

            page_cache: 30GB (indexes should be fitting in the page cache so set it to 30GB)
            heap_init: 27GB
            heap_max: 27GB

            16 Core 64 GB RAM
                9737247: (Users)
                    10000 -> 128s
                        page_cache: 8GB
                        heap_init: 12GB
                        heap_max: 12GB
                    100000 -> 223s

                42850538: (Posts)
                    10000 -> 504s

                * While creating relations in parallel mode we were getting NullPointException so tried without it

                42388348: (Relations)
                    10000 -> 2207s

                53806: (Tag)
                    1000 -> 1

                25908201: (Post - Post)
                    1000 -> 1403

        * Problems Faced:
            * Couldn't delete nodes
            * Server Got Hung
            * Unable to connect to the neo4j server

    2) Functionality
        1) Using Centralities
        2) Full Text Search
        3)
