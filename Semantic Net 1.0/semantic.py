# Author: Chris Malitsky
# This is version 1.0 of the Semantic Network with Analogical Reasoning Integration
# Utilizes a Dictionary of tuples that describe components of a network graph

# List of options with explanations:
#  0. Exit Program              -- Closes the program
#  1. Print Graphs              -- Prints all the available graphs for observation
#  2. Add Graph                 -- Allows user to specify the name of the graph and start adding nodes/relationships
#  3. Compare two graphs        -- Allows user to compare two graphs to see if they are a perfect match or not
#  4. Knowledge Query           -- Applies a rudimentary front end that also has basic NLP when asking the system to present information about a certain dictionary key
#  5. Find Matches              -- Displays match information pertaining to a user specified graph in regards to all the other graphs in the system
#  55. Print Options            -- Displays the available user options (this menu)

# Match Info:
# Three possibilitis: Perfect Match, Match, or Not Even Close
# 1. Perfect Match - if a graph is a perfect match with another graph, the two graphs are exactly the same - this is the best match option
# 2. Match - if two graphs have similar attributes, they are a match
#       This is further broken down into a point system:
#           Same subject        -------> 1 Point
#           Same relationship   -------> 1 Point
#           Same thing          -------> 1 Point   (A thing is just what a subject links with via a relationship)
#       The idea is that if two graphs are not a perfect match (ideal), but have nodes/relationships in common, the graph with the most points is the best match
#       Each node-relationship-node tuple is compared with all other node-relationship-node tuples of another graph resulting in a sort of cartesian product
# 3. Not Even Close - if two graphs share nothing in common at all, they are Not Even Close to each other

avail_graphs = {}

avail_graphs["dog1"] = [("have", "dogs", "tails"),
                        ("like to", "dogs", "bark"), 
                        ("really like", "dogs", "treats"),
                        ("enjoy", "dogs", "running")]

avail_graphs["dog2"] = [("have", "dogs", "tails"),
                        ("like to", "dogs", "bark"), 
                        ("really like", "dogs", "treats"),
                        ("enjoy", "dogs", "running")]

avail_graphs["cats"] = [("have", "cats", "tails"),
                        ("like to", "cats", "meow"),
                        ("really like", "cats", "treats"),
                        ("enjoy", "cats", "sleeping")]

avail_graphs["human"] = [("listen to", "humans", "music"),
                         ("cannot stand", "humans", "traffic")]


def new_graph():
    name = input("Now adding new graph. What should the graph's name be?")
    new = []
    avail_graphs[name] = new
    running = True

    while(running):
        
        node1 = input("Enter node 1: ")
        node2 = input("Enter node 2: ")
        rel = input("Enter relationship: ")

        avail_graphs[name].append([rel, node1, node2])

        check_done = input("If done, press X, to add another node, press Enter")

        if(check_done == 'X' or check_done == 'x'):
            running = False

def print_info(graph, thing):
    entry_num = 0
    indeces = []
    
    for index, item in enumerate(graph):
        if thing == item[1]:
            entry_num += 1
            indeces.append(index)
        
    if entry_num == 1:
        curr = graph[indeces[0]]
        print(curr[1], curr[0], curr[2])
    
    elif entry_num == 2:
        curr1 = graph[indeces[0]]
        curr2 = graph[indeces[1]]
        print(curr1[1], curr1[0], curr1[2] + " and " + curr2[0], curr2[2])
            
    elif entry_num > 2:
        j = 1
        curr = graph[0]
        print(curr[1], curr[0], curr[2], end=', ')
        while j < len(indeces):
            curr = graph[indeces[j]]
            if(j == len(indeces)-1):
                print("and " + curr[0], curr[2])
            else:
                print(curr[0], curr[2], end=', ')
            j += 1 
    else:
        print("I'm sorry, I didn't catch that")

def compare(graph1, graph2):
    perfect_match = False
    exact_matches = 0
    total_points = 0
    for i in graph1:
        subject_one = i[1]
        relationship_one = i[0]
        thing_one = i[2]
        for j in graph2:
            exact_match = True
            subject_two = j[1]
            relationship_two = j[0]
            thing_two = j[2]

            if(subject_one == subject_two):
                total_points += 1
            else:
                exact_match = False
            if(relationship_one == relationship_two):
                total_points += 1
            else:
                exact_match = False
            if(thing_one == thing_two):
                total_points += 1
            else:
                exact_match = False

            if(exact_match == True):
                exact_matches += 1
                break

    if(len(graph1) == len(graph2) and len(graph1) == exact_matches):
        perfect_match = True

    return (exact_matches, total_points, perfect_match)

def find_matches(graph):
    cont = False
    results = []
    for (key, value) in avail_graphs.items():
        if key == graph:
            arr = value
            cont = True
    
    if cont == True:
        for (key, value) in avail_graphs.items():
            if key != graph:
                match_results = compare(arr, value)
                if(match_results[2] == True):
                    results.append(('Perfect Match', key, arr, value, match_results[0], match_results[1]))
                elif(match_results[1] > 0):
                    results.append(('Match', key, arr, value, match_results[0], match_results[1]))
                else:
                    results.append(('Not Even Close', key, arr, value, match_results[0], match_results[1]))
    else:
        print("No matches found")

    return results


def print_options():
    print(
    '''
    0. Exit Program
    1. Print Graphs
    2. Add Graph
    3. Compare two graphs
    4. Knowledge Query
    5. Find Matches
    55. Print Options
    ''')

def main():
    running = True
    print_options()
    while(running):
        answer = int(input("Select an Option:"))
        if(answer == 0):
            running = False
        elif(answer == 1):
            for (key, value) in avail_graphs.items():
                print(key, value)
        elif(answer == 2):
            new_graph()
        elif(answer == 3):
            graph1_name = input("Graph 1:")
            graph2_name = input("Graph 2:")
            for (key, value) in avail_graphs.items():
                if key == graph1_name:
                    graph1 = value
                elif key == graph2_name:
                    graph2 = value
            test = compare(graph1, graph2) 
            if (test[2] == True):
                print("Perfect Match")
        elif(answer == 4):
            found = False
            know = input("What would you like to know about?")
            for (key,value) in avail_graphs.items():
                if key == know and found == False:
                    found = True
                    arr = value
                    curr = value[0]
                    title = curr[1]
                    print_info(arr, title)
            if found == False:
                print("Sorry I do not know what you mean")
        elif(answer == 5):
            perfect = []
            match = []
            no_match = []
            graph = input("What graph do you want to conduct matching on?")
            matches = find_matches(graph)
            if matches is None:
                print("No matches")
            else:
                for i in matches:
                    if(i[0] == 'Perfect Match'):
                        perfect.append(i)
                    elif(i[0] == 'Not Even Close'):
                        no_match.append(i)
                    elif(i[0] == 'Match'):
                        match.append(i)
                print('\nResults:')
                if(len(perfect) > 0):
                    print('Perfect Matches: ', len(perfect))
                    for i in perfect:
                        print("",i[1], ":", i[3])
                    print()
                else:
                    print("No Perfect Matches")
                    print()
                    if(len(match) > 0):
                        print("Rough Matches: ", len(match))
                        for i in match:
                            print("",i[1], ":", i[3], "Points: ", i[5])
                        print()
                    else:
                        print("No Rough Matches")
                        print()
                    if(len(no_match) > 0):
                        print("Not Even Close: ", len(no_match))
                        for i in no_match:
                            print("",i[1], ":", i[3])
                        print()
                    else:
                        print("Nothing matches anywhere")
                        print()
        elif(answer == 55):
            print_options()
        else:
            print("Sorry, not an available option")

if __name__ == "__main__":
    main()