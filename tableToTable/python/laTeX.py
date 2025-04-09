
def getFormula(cellsList, textList):

    cells = []
    for row in cellsList:
        cells.append([])
        for cell in row:
            width = cell[2] - cell[0]
            cells[-1].append(width)

    widthsCompare = max(cells, key=len) # 335, 320 # the max rows

    colString = ''
    for i in range(len(widthsCompare)):
        colString += '|l'
    colString += '|'

    print('\\documentclass{article}')
    print('\\usepackage{multirow}')
    print('\\usepackage{booktabs}')
    print('\\begin{document}')
    print('\\begin{table}[h]')
    print('\\centering')
    print(f'\\begin{{tabular}}{{{colString}}}')
    print('\\hline')

    for textRow, widthRow in zip(textList, cells):
        string = ''
        for text, width, i in zip(textRow, widthRow, range(len(widthsCompare))):

            if width == widthsCompare[i]:
                string += f'\\verb|{text}|&'
            else:
                summedWidth = widthsCompare[i]
                count = 1
                while width != summedWidth:
                    count += 1
                    i += 1
                    summedWidth += widthsCompare[i]
                string += f'\\multicolumn{{{count}}}{{|c|}}{{\\texttt{{{text}}}}}&'

        string = string[:-1] # removes last &s
        string += '\\\\'
        print(string)
        print('\\hline')

    print('\\end{tabular}')
    print('\\end{table}')
    print('\\end{document}')
