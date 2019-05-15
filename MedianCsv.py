def main():
    from pathlib import Path
    from os import listdir
    from csv import writer, reader
    directory = Path.cwd()
    files = listdir(directory)
    TextFiles = filter(lambda x: x.startswith('frames.'), files)
    textFiles = list(filter(lambda x: x.endswith('.csv'), TextFiles))
    print(textFiles)
    for i in range(0, len(textFiles)):
        file_first = textFiles[i]
        FILENAME = textFiles[i]
        DataSet = list()
        with open(FILENAME, "r", newline="") as file:  ### жесткий костыль
            read = reader(file)
            for row in read:
                element = row[1]
                DataSet.append([row[0], row[1], row[2], row[3]])
        score=0
        score_elem=element
        now_score_elem=element
        now_score=0
        with open(FILENAME, "r", newline="") as file:
            read = reader(file)
            for row in read:

                next_elem =row[1]
                if (element == next_elem):
                    if (score ==0):
                        score+=1
                        score_elem=element
                else:
                    now_score+=1
                    now_score_elem=next_elem
            if (now_score>score and score_elem !=now_score_elem ):
                 score=now_score
                 score_elem=now_score_elem
                 now_score=0
                 now_score_elem=None
            print('Score ',score,' Elem',element)

        for i in range (0,len(DataSet)):
            DataSet[i][1]=element
        FILENAME = "{id}".format(id='Median_'+FILENAME)
        with open(FILENAME, "w", newline="") as file:
            writ = writer(file)
            writ.writerows(DataSet)
            print("Created csv file")
    return 0
main()