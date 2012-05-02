============================
Common operations comparison
============================
Here we briefly consider some common operations with MongoDB data in
vanilla Mongoshell, ``Pymongo`` and ``Minimongo`` DOM.

Initialization
--------------

Suppose we have ``mongod`` instance running on port 27018. Here's how we init
connection on db ``test`` and collection ``test_model`` with unique descendingly-ordered
index on field ``x``.

**Mongoshell**::

    use test
    db.test_model.ensureIndex({x:-1},{unique:true})

**Pymongo**::

    import pymongo
    conn = pymongo.Connection(‘localhost’, 27018)
    db = conn.test
    db.test_model.ensure_index([("x", pymongo.DESCENDING)], unique=True)

**Minimongo**:

Configure is invoked once for all models in app::

    from minimongo import Model, Index, configure
    configure(port=27018)
    class TestModel(Model):
        class Meta:
            database = ‘test’
            collection = ‘test_model’
            indices = ( Index([("x", pymongo.DESCENDING)], unique=True ), )

Insert
------

**Mongoshell**::

    db.test_model.insert({x: 1,y: {y1: 2,y2: 2}})

**Pymongo**::

    db.test_model.insert({"x": 1, "y" :{"y1": 2,"y2": 2}})

**Minimongo**::

    test_elem = TestModel(x=1,y={"y1":2,"y2":2})
    # Could be done as test_elem = TestModel({"x": 1, "y": {"y1":2,"y2":2}})
    test_elem.save()

Update
------

Set another value to ``y.y1``.

**Mongoshell**::

    db.test_model.update({x: 1}, {$set: {"y.y1" : 2}})

**Pymongo**::

    db.test_model.update({"x": 1}, {"$set": {"y.y1": 2}})

**Minimongo**::

    test_elem.load({“y”:1}) # load last version of document, maybe it was changed
    test_elem.y.y1 = 3
    test_elem.save()

Remove field
------------

Remove field ``y``.

**Mongoshell**::

    db.test_model.update({x: 1}, {$unset: {y: 1}})

**Pymongo**::

    db.test_model.update({"x": 1}, {"$unset": {"y": 1}})

**Minimongo**::

    del test_elem.y
    test_elem.save()

Find and remove document
------------------------

Remove document where ``z`` contains 1.

**Mongoshell**::

    db.test_model.insert({x: 2, z: [1,2]})
    db.test_model.remove({z: 1})

**Pymongo**::

    db.test_model.insert({"x": 2, "z": [1,2]})
    db.test_model.remove({"z": 1})

**Minimongo**::

    test_elem_2 = TestModel(x=1,z=[1,2]).save()
    test_elem_2_cp = TestModel.collection.find_one({"z":1})
    assert test_elem_2 == test_elem_2_cp
    test_elem_2_cp.remove()
