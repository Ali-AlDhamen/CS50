from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
   Or(AKnight,AKnave), # can be only one knight or knave
   Not(And(AKnight,AKnave)), # cant be both
   Implication(AKnight, And(AKnave,AKnight)), # if hes knight then he can be both else he`s not
   Implication(AKnave, Not(And(AKnave,AKnight))) # if hes Knave then he`s not both because hes lying
   
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
   Or(AKnight,AKnave), # can be only one knight or knave
   Not(And(AKnight,AKnave)), # cant be both
   Or(BKnight,BKnave), # can be only one knight or knave
   Not(And(BKnight,BKnave)), # cant be both
   Implication(AKnight, And(AKnave,BKnave)), # if A is a knight then his sentence is true else wrong
   Implication(AKnave, Not(And(AKnave,BKnave))), # if A is knave then his sentence is wrong and that makes B Knight
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
   Or(AKnight,AKnave), # can be only one knight or knave
   Not(And(AKnight,AKnave)), # cant be both
   Or(BKnight,BKnave), # can be only one knight or knave
   Not(And(BKnight,BKnave)), # cant be both
   Implication(AKnight, And(AKnight,BKnight)), # if A is right then they r both knights
   Implication(AKnave, And(AKnave,BKnight)), # if A is lair then they are not same 
   Implication(BKnight, And(BKnight,AKnave)), # if B is right then they r different so that makes A a Knave 
   Implication(BKnave, And(BKnave,AKnave)) # if B is lair then they are same
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
   Or(AKnight,AKnave), # can be only one knight or knave
   Not(And(AKnight,AKnave)), # cant be both
   Or(BKnight,BKnave), # can be only one knight or knave
   Not(And(BKnight,BKnave)), # cant be both
   Or(CKnight,CKnave), # can be only one knight or knave
   Not(And(CKnight,CKnave)), # cant be both
   Implication(AKnight, Or(AKnave, AKnight)), # if A is right then hes either knight or knave 
   Implication(AKnave, Not(Or(AKnave, AKnight))),# if A is lair then hes one for sure
   Implication(BKnight, And(CKnave, AKnave)), # if B is right then Both A and C are Knaves 
   Implication(BKnave, Not(And(CKnave, AKnave))), # if B is lair then Both A and C are not Knaves so they are knights
   Implication(CKnight, AKnight), # if C is right then A is knight 
   Implication(CKnave, Not(AKnight)),# if C is lair then A is not knight aka knave
   
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
