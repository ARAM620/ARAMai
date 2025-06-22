#command_parser.py

from konlpy.tag import Mecab

mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")

def extract_app_name(command: str) -> str:
    tokens = mecab.pos(command)
    nouns = [word for word, pos in tokens if pos in ('NNG', 'NNP')]
    return max(nouns, key=len) if nouns else ""
