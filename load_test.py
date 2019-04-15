
import fire


def log_time():
    def decorator(func):
        def handler(*args, **kwargs):
            import datetime
            import time
            print('Start Time: {} {}'.format(
                func.__name__, datetime.datetime.now()))
            a = time.time()
            func(*args, **kwargs)
            b = time.time()
            print('End Time: {} {}'.format(
                func.__name__, datetime.datetime.now()))
            print('ElapsedTime(in seconds) for function {}: {}'.format(
                func.__name__, b-a))
        handler.__doc__ = func.__doc__
        return handler

    return decorator


@log_time()
def load_test(batch_size):
    from neomodel import config

    config.DATABASE_URL = 'bolt://{}:{}@{}:{}'.format(
        'neo4j', 'neon', 'localhost', 7687
    )
    options = "{batchSize: "+str(batch_size) + \
        ", iterateList: true, parallel: true}"

    def run_cypher(arg1, arg2):
        from neomodel import db

        query = """CALL apoc.periodic.iterate("{}","{}", {});""".format(
            arg1, arg2, options
        )
        results, meta = db.cypher_query(query)
        return results, meta

    def create_unique_constraints():
        from neomodel import db
        queries = [
            "create index on :Post(title);",
            "create index on :Post(createdAt);",
            "create index on :Post(score);",
            "create index on :Post(views);",
            "create index on :Post(favorites);",
            "create index on :Post(answers);",
            "create index on :Post(score);",

            "create index on :User(name);",
            "create index on :User(createdAt);",
            "create index on :User(reputation);",
            "create index on :User(age);",

            "create index on :Tag(count);",

            "create constraint on (t:Tag) assert t.tagId is unique;",
            "create constraint on (u:User) assert u.userId is unique;",
            "create constraint on (p:Post) assert p.postId is unique;",

        ]
        for query in queries:
            db.cypher_query(query)
        return

    @log_time()
    def load_posts():
        arg1 = 'CALL apoc.load.csv(\'file:///import/posts.csv\') YIELD lineNo, map as row, list return row'
        arg2 = 'MERGE (post: Post {id:row.`postId:ID(Post)`}) ON CREATE SET post.title = row.title, post.body = row.body, post.score = row.score, post.views = row.views, post.comments = row.comments;'
        run_cypher(arg1, arg2)

    @log_time()
    def load_users():
        arg1 = 'CALL apoc.load.csv(\'file:///import/users.csv\') YIELD lineNo, map as row, list return row'
        arg2 = 'MERGE(owner:User {id: row.`userId: ID(User)`}) ON CREATE SET owner.displayname=row.displayname, owner.reputation=row.reputation,owner.aboutme=row.aboutme,owner.websiteurl=row.websiteurl,owner.location=row.location,owner.profileimageurl=row.profileimageurl,owner.views=row.views,owner.upvotes=row.upvotes,owner.downvotes=row.downvotes'
        run_cypher(arg1, arg2)

    @log_time()
    def load_tags():
        arg1 = 'CALL apoc.load.csv(\'file:///import/tags.csv\') YIELD lineNo, map as row, list return row'
        arg2 = 'MERGE (tag: Tag {id:row.`tagId:ID(Tag)`})'
        run_cypher(arg1, arg2)

    @log_time()
    def load_tag_posts_rel():
        arg1 = 'CALL apoc.load.csv(\'file:///import/tags_posts_rel.csv\') YIELD lineNo, map as row, list return row'
        arg2 = 'MATCH (tag:Tag {id:apoc.convert.toString(row.`:END_ID(Tag)`)}) MATCH (post:Post {id:apoc.convert.toString(row.`:START_ID(Post)`)}) MERGE (post)-[:TAGGED]->(tag);'
        run_cypher(arg1, arg2)

    @log_time()
    def load_posts_rel():
        arg1 = 'CALL apoc.load.csv(\'file:///import/posts_rel.csv\') YIELD lineNo, map as row, list return row'
        arg2 = 'MATCH (child_post:Post {id:apoc.convert.toString(row.`:END_ID(Post)`)}) MATCH (parent_post:Post {id:apoc.convert.toString(row.`:START_ID(Post)`)}) MERGE (parent_post)-[:PARENT_OF]->(child_post);'
        run_cypher(arg1, arg2)

    @log_time()
    def load_user_posts():
        arg1 = 'CALL apoc.load.csv(\'file:///import/user_posts_rel.csv\') YIELD lineNo, map as row, list return row'
        arg2 = 'MATCH (post:Post {id:apoc.convert.toString(row.`:END_ID(Post)`)}) MATCH (owner:User {id:apoc.convert.toString(row.`:START_ID(User)`)}) MERGE (owner)-[:ASKED]->(post);'
        run_cypher(arg1, arg2)

    create_unique_constraints()
    load_posts()
    load_users()
    load_tags()
    load_user_posts()
    load_posts_rel()
    load_tag_posts_rel()


class LoadTest():

    def load_test(self, batch_size=1000):
        load_test(batch_size)


if __name__ == '__main__':
    fire.Fire(LoadTest)
