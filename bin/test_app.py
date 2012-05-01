import config_options
from minimongo.model import CASCADE
from minimongo import Model, Index, configure

configure(config_options)

class Author(Model):
    class Meta:
        database = 'minimongo'
        collection = 'author'
        indices = ( Index("first_name", unique=True), )

class Post(Model):
    class Meta:
        database = 'minimongo'
        collection = 'post'
        references = ( ("author", Author, CASCADE), ) # field_name : class_name : type

p = Post.collection.find_one({"time":{"$exists":"true"}})
print p


#posts = Post.collection.find({"content":"Second post"})
#for post in posts:
#    print post

#auth1 = Author.collection.find_one({"last_name":{"$regex":"laso"}})
#ref = auth1.dbref()
#Post.collection.update({"content":"superior"}, {"$set":{"author":ref}})
#c = Post.collection.find({"author":auth1.dbref()}).count()
#p = Post(content="Superior!", author=auth1.dbref())
#p.save()
#auth1.remove()
#auth1.midname = "Igorevich!"
#auth1.save()

#a = Author(first_name="Dmitrii", last_name="Vlasov")
#p = Post(author=a.dbref(), content="hello")
#a.save()
#p.save()

#auth1.remove()

#author_dbref = author.dbref()
#post = Post.collection.find_one({"author":author_dbref})
#post1 = Post.collection.find_one({"author":{"$exists":"true"}})
#post1.author = author.dbref()
#post1.save()