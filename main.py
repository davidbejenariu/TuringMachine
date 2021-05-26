from dataclasses import dataclass
tapeLimit = 1000000


@dataclass()
class TuringMachine:
    blank: str
    alphabet: set
    states: set
    initialState: str
    acceptState: str
    rejectState: str
    transitions: dict

    def __init__(self, inputFile):
        with open(inputFile, "r") as file:
            self.blank = file.readline()[0]

            self.alphabet = set()
            for s in file.readline().split():
                self.alphabet.add(s)

            self.states = set()
            for s in file.readline().split():
                self.states.add(s)

            self.initialState = file.readline().replace("\n", "")
            self.acceptState = file.readline().replace("\n", "")
            self.rejectState = file.readline().replace("\n", "")

            self.transitions = dict()
            for line in file.readlines():
                transition = line.replace("\n", "").split()
                key = (transition[0], transition[1])
                value = (transition[2], transition[3], transition[4])

                self.transitions[key] = value

    def checkWord(self, word):
        """
            generez de fiecare data un tape de lungime tapeLimit care incepe cu blank (#), contine cuvantul de verificat in mijloc si se
            termina tot cu blank (#), astfel ca ne putem deplasa si in stanga, cu o limita totusi, data de tapeLimit (un milion este o limita
            rezonabila pentru tape la acest proiect, sper)
        """
        toFill = int(tapeLimit - len(word) / 2)
        tape = [self.blank] * toFill + list(word) + [self.blank] * toFill

        state = self.initialState
        pos = toFill

        while state != self.acceptState and state != self.rejectState:
            transition = self.transitions[(state, tape[pos])]
            state = transition[0]
            tape[pos] = transition[1]

            if transition[2] == '>':
                pos += 1
            elif transition[2] == '<':
                pos -= 1

        return state == self.acceptState


if __name__ == '__main__':
    machine = TuringMachine("input.in")
    print(machine)

    print("Test your words:")
    word = input()

    # presupunem ca 'quit' e cuvant rezervat programului si nu poate fi verificat de vreo masina Turing :)
    while word != "quit":
        if machine.checkWord(word):
            print("Accepted")
        else:
            print("Rejected")

        word = input()
