from arquivo import ArquivosRegulares

arquivo1 = ArquivosRegulares('novo', 'jfdadfçlakjçlfkçlkajçlkdfjjdjsksksk k')
arquivo2 = ArquivosRegulares('', '')
arquivo2.load_parse(arquivo1.save_format())
assert arquivo2.get_nome() == 'novo'
assert arquivo2.get_dado() == 'jfdadf?lakj?lfk?lkaj?lkdfjjdjsksksk k'
