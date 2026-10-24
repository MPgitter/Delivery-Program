

#Hashmap class
class CreateHashTable:
    def __init__(self , capacity = 20):
        self.table = []
        for i in range(capacity):
            self.table.append([])

    # Citing source: WGU code repository W-2_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy.py
    def insert(self,key,item): #Inserts and updates the hash table
        bucket = hash(key) % len(self.table)
        bucket_index = self.table[bucket]

        #if there is already a key then update the key
        for kv in bucket_index: #0(n)
            #print key value
            if kv[1] == key:
                kv[1] = item
                return True

        #If key is not in the bucket then add key to it
        key_value = (key, item)
        bucket_index.append(key_value)
        return True

    #For looking up items in hash table
    def lookup(self,key):
        bucket= hash(key) % len(self.table)
        bucket_index= self.table[bucket]
        for pair in bucket_index:
            if key == pair[0]:
                return pair[1]
        return None

#Removes packages from hash table
    def remove(self,key):
        bucket= hash(key) % len(self.table)
        bucket_index= self.table[bucket]

        #if key found then remove from table
        if key in bucket_index:
            bucket_index.remove(key)