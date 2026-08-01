import sys
from antlr4 import *
from InfraLangLexer import InfraLangLexer
from InfraLangParser import InfraLangParser
from AWSInfraListener import AWSInfraListener

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = InfraLangLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = InfraLangParser(stream)
    tree = parser.infra()

    listener = AWSInfraListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    listener.deploy()

if __name__ == "__main__":
    main(sys.argv)
