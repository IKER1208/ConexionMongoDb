from pymongo import MongoClient, errors

def conectar_mongo():
    try:
        client = MongoClient(
           "mongodb+srv://admin:admin@myatlasclusteredu.oh7cbmy.mongodb.net/",
            serverSelectionTimeoutMS=3000
        )
        client.admin.command("ping")
        print("✅ Conexión exitosa a MongoDB Atlas.")
        return client
    except errors.PyMongoError:
        print(f"❌ Error al conectar a MongoDB")
        return None
    