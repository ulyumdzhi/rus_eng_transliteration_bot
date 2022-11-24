import logging
import typing

from trans import transliteration_dict


def trans_checker(word: str) -> typing.Tuple[int, typing.Any]:
    
    LIGAL = ['-', '–','`',"'"]

    _word = []
    
    for index, _symbol in enumerate(word):
        if _symbol in LIGAL:
            _word.append(_symbol)
        else:
            try:
                _symbol = transliteration_dict[_symbol.upper()]
                _word.append(_symbol)
            except Exception as e:
                logging.info(f'{word=} | {_symbol=} | Exception: {e}')
                return 0, index
    
    return 1, ''.join(_word)
