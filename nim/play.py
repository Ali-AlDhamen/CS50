from nim import train, play

training_times = int(input('How many times you want to train it: '))
ai = train(training_times)
play(ai)
