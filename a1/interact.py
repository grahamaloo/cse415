import grahamtk

agent = grahamtk.CrazyJoe()
print(agent.introduce())
while True:
    the_input = input('User: ')
    if the_input == "bye" or the_input == "exit" or the_input == "close" or the_input == "quit":
        print('Goodbye!')
        break
    print(agent.agentName() + ': ' + agent.respond(the_input))