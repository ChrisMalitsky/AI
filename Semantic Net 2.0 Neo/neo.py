from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = "password"

driver = GraphDatabase.driver(uri, auth=(user, password))

def run_query(query):
    with driver.session() as session:
        results = session.run(query)

    return results

def print_all():
    query = "MATCH (n)-[r]->(m) RETURN n, type(r), m"
    results = run_query(query)
    for n in results:
        print(n[0]["name"], n[1], n[2]["name"])

def print_specific():
    answer = input("What would you like to know about? ")
    query = "MATCH (n:%s)-[r]->(m) RETURN n, type(r), m" % answer
    results = run_query(query)
    if(results.peek() is None):
        print("Sorry, I do not know about that")
    else:
        for n in results:
            print(n[0]["name"], n[1], n[2]["name"])

def add_node(name):
    query = "Create(%s:%s{name:'%s'})" %(name,name,name)
    results = run_query(query)
    print("Node %s added" % name)
    print(results)

def new_node_relationship(name1, relationship, name2):
    query = "Create (%s:%s{name:'%s'})-[r:%s]->(%s:%s{name:'%s'})" % (name1, name1, name1, relationship, name2, name2, name2)
    run_query(query)
    print("Added node relationship: %s %s %s" % (name1, relationship, name2))
    prompt_new(name2)

def existing_node_relationship(name1, relationship, name2):
    query = "MATCH (a:%s),(b:%s) create (a)-[r:%s]->(b)" % (name1, name2, relationship)
    results = run_query(query)
    if results is None:
        print("Sorry, one or both of those nodes do not exist")
    else:
        print(name1, relationship, name2)

def node_relationship_new_node(name1, relationship, name2):
    query = "MATCH (a:%s) create (a)-[r:%s]->(%s:%s{name:'%s'})" % (name1, relationship, name2, name2, name2)
    results = run_query(query)
    if results is None:
        print("Sorry, no results for %s" % name1)
    else:
        print(name1, relationship, name2)
        prompt_new(name2)

def delete_node(name):
    query = "MATCH (a:%s) DETACH DELETE a" % name
    answer = input("Deleting a node deletes all relationships associated with it, proceed? (y/n)")
    if(answer == 'y' or answer == 'Y'):
        run_query(query)
        print("Removed %s" % name)
    else:
        print("Aborted")

def delete_relationship(name1, relationship, name2):
    query = "MATCH (n:%s)-[r:%s]->(m:%s) DELETE r" % (name1, relationship, name2)
    answer = input("You will be deleting the relationship: %s %s %s, proceed?" % (name1, relationship, name2))
    if(answer == 'y'):
        run_query(query)
        print("Deleted %s %s %s" % (name1, relationship, name2))
    else:
        print("Aborting")

def prompt_new(name1):
    # query = "MATCH (n:%s {name:'%s'}) where n.name='%s' RETURN n.name" % (name1, name1, name1)
    # results = run_query(query)
    # print(results)
    answer = input("What is %s?" % name1)
    relation = input("What is the relationship between %s and %s" % (name1, answer))
    if not does_node_exist(answer):
        node_relationship_new_node(name1, relation, answer)
        
    else:
        existing_node_relationship(name1, relation, answer)
    
    # print("Thank you for telling me about %s and %s" % (name1, answer)

            
    # if results.peek() is None: 
    #     answer = input("What is %s?" % name1)
    #     new_query = "MATCH (n:%s {name:'%s'}) where n.name='%s' RETURN n.name" % (answer, answer, answer)
    #     new_result = run_query(new_query)
    #     relation = input("Enter the relationship between %s and %s" % (name1, answer))
    #     if(new_result.peek() is None):
    #         relation = input("Enter the relationship between %s and %s" % (name1, answer))

    # else:
    #     for n in results:
    #         print(n[0])

def does_relationship_exist(name1, relationship, name2):
    query = "MATCH (n:%s)-[r:%s]->(m:%s) RETURN n, type(r), m" (name1, relationship, name2)
    results = run_query(query)
    if(results.peek() is None):
        return False
    else:
        return True

def does_node_exist(name1):
    query = "MATCH (n:%s {name:'%s'}) where n.name='%s' RETURN n.name" % (name1, name1, name1)
    results = run_query(query)
    if(results.peek() is None):
        return False
    else:
        return True
    
def purge():
    query = "MATCH (n) detach delete n"
    run_query(query)
    print("Removed everything")

def main():
    run = True

    print("Welcome to NEO, to view Network, go to localhost:7474")
    options = '''Select your option:
    0. Show options
    1. Print all relationships
    2. Show relationships for specified value
    3. Add a new relationship with existing nodes
    4. Add a new relationship with new nodes
    5. Add new relationship from existing node to new node
    6. Remove a node
    7. Remove a relationship
    8. PURGE
    9. Stop the program'''
    print(options)

    while(run):
        answer = int(input("Select option: "))
        if(answer == 0):
            print(options)
        elif(answer == 1):
            print_all()
        elif(answer == 2):
            print_specific()
        elif(answer == 3):
            subject1 = input("What is the first node?")
            subject2 = input("What is the second node?")
            relationship = input("What is their relationship?")
            existing_node_relationship(subject1, relationship, subject2)
        elif(answer == 4):
            subject1 = input("What is the first node?")
            subject2 = input("What is the second node?")
            relationship = input("What is their relationship?")
            new_node_relationship(subject1, relationship, subject2)
        elif(answer == 5):
            subject1 = input("What is the first node?")
            subject2 = input("What is the second node?")
            relationship = input("What is their relationship?")
            node_relationship_new_node(subject1, relationship, subject2)
        elif(answer == 6):
            answer = input("Which node do you want to delete?")
            delete_node(answer)
        elif(answer == 7):
            subject1 = input("What is the first node?")
            subject2 = input("What is the second node?")
            relationship = input("What is their relationship?")
            delete_relationship(subject1, relationship, subject2)
        elif(answer == 8):
            answer = input("Purging removes all things from database, are you sure? (y/n)")
            if(answer == 'y'):
                answer_check = input("Are you super sure?")
                if(answer_check == 'y'):
                    purge()
                else:
                    print("Not deleting")
            else:
                print("not deleting")
        elif (answer == 9):
            run = False

if __name__ == "__main__":
    main()