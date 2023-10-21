import json
import os

with open("data/name.json", "r", encoding="utf-8") as data:
    name_data = json.load(data)

with open("data/text.json", "r", encoding="utf-8") as data:
    text_data = json.load(data)

with open("data/spelling.json","r",encoding="utf-8") as data:
    spelling_data = json.load(data)

class jsonManager:
    def addGroup(self, new_data:str) -> None:
        with open("cache/joined_group.json", "r+", encoding="UTF-8") as file:
            file_data = json.load(file)
            file_data["groups"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)

    def groupLen(self) -> None:
        with open("cache/joined_group.json", "r", encoding="utf-8") as data:
            data = json.load(data)
        return len(data["groups"])

    def exist(self, chat_id:int) -> bool:
        with open("cache/joined_group.json", "r", encoding="utf-8") as data:
            data = json.load(data)
        try:
            for i,j in data["groups"]:
                if i == chat_id:
                    return True
            return False
        except Exception:
            return False
        
    def getIds(self):
        with open("cache/joined_group.json", "r", encoding="utf-8") as data:
            data = json.load(data)
        ids = []
        for i,j in data["groups"]:
            ids.append(i)
        return ids
    
    def getSpelling(self, index_num):
        return list(spelling_data["spelling"][index_num])
    
    def spellingLen(self):
        return len(spelling_data["spelling"])

    def check(self, chat_id:int ,text:str, index:int):
        with open("data/words.txt", "r", encoding="UTF-8") as file:
            for i in file:
                if text.lower() == i.strip():
                    self.addWords(chat_id, text)
                    if len(text) == 4 or len(text) == 5:
                        self.increaseScore(chat_id, 1)
                        return text_data["one_point"]
                    elif len(text) == 6:
                        self.increaseScore(chat_id, 3)
                        return text_data["three_point"]
                    elif len(text) == 7 and sorted(list(text)) == sorted(spelling_data["spelling"][index]):
                        self.increaseScore(chat_id, 7)
                        return text_data["seven_point"]
                    elif len(text) == 7:
                        self.increaseScore(chat_id, 5)
                        return text_data["five_point"]
                    else:
                        pass
        return text_data["incorrect"]
    
    def increaseScore(self, chat_id:int, point:int):
        with open("cache/score.json", "r", encoding="UTF-8") as data:
            data = json.load(data)
        
        for i,j in enumerate(data["score"]):
            if j[0] == chat_id:
                with open("cache/score.json", "r+", encoding="UTF-8") as file:
                    file_data = json.load(file)
                    file_data["score"][i][2] += point
                    file.seek(0)
                    json.dump(file_data, file, indent = 4)
                    return
    
    def addTotalScore(self,new_data) -> None:
        with open("cache/total_score.json", "r+", encoding="UTF-8") as file:
            file_data = json.load(file)
            file_data["score"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)

    def addScore(self,new_data) -> None:
        with open("cache/score.json", "r+", encoding="UTF-8") as file:
            file_data = json.load(file)
            file_data["score"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)

    def createTotalScore(self):
        with open("cache/joined_group.json", "r", encoding="UTF-8") as data:
            data = json.load(data)
        for i,j in data["groups"]:
            self.addTotalScore([i,j,0,[]])

    def createScore(self):
        with open("cache/joined_group.json", "r", encoding="UTF-8") as data:
            data = json.load(data)
        for i,j in data["groups"]:
            self.addScore([i,j,0,[]])
    
    def wordExist(self,chat_id:int, text:str):
        with open("cache/score.json", "r", encoding="UTF-8") as data:
            data = json.load(data)
        words = []
        for i,j in enumerate(data["score"]):
            if j[0] == chat_id:
                words = data["score"][i][-1]
                break
        return True if text.lower() in words else False
    
    def addWords(self,chat_id:int,word):
        with open("cache/score.json", "r", encoding="UTF-8") as data:
             data = json.load(data)
        for i,j in enumerate(data["score"]):
            if j[0] == chat_id:
                with open("cache/score.json", "r+", encoding="UTF-8") as file:
                    file_data = json.load(file)
                    file_data["score"][i][-1].append(word.lower())
                    file.seek(0)
                    json.dump(file_data, file, indent = 4)
                return
    def initialPoint(self):
        result = []
        with open("cache/joined_group.json", "r", encoding="UTF-8") as data:
            for i in json.load(data)["groups"]:
                result.append((i[1],0))
        return result

    def getPoint(self):
        result = []
        with open("cache/score.json", "r", encoding="UTF-8") as data:
            for i in json.load(data)["score"]:
                result.append((i[1],i[2]))
        result = sorted(result,key=lambda x:x[1])[::-1]
        return result
    def reset(self):
        for i in ["total_score.json", "score.json"]:
            os.remove(f"cache/{i}")

        with open("cache/total_score.json","w") as data:
            data.write(json.dumps({"score":[]}, indent=4))
        with open("cache/score.json","w") as data:
            data.write(json.dumps({"score":[]}, indent=4))
        
        self.createScore()
        self.createTotalScore()


    def removeSpellings(self,final_page):
        if final_page == False:
            with open("cache/total_score.json","r+", encoding="utf-8") as write_data:
                with open("cache/score.json","r") as read_data:

                    write_data_j = json.load(write_data)
                    read_data_j = json.load(read_data)

                    for j,i in enumerate(read_data_j["score"]):
                        write_data_j["score"][j][2] += i[2]
                    write_data.seek(0)
                    json.dump(write_data_j, write_data, indent = 4)

            os.remove(f"cache/score.json")

            with open("cache/score.json","w") as data:
                data.write(json.dumps({"score":[]}, indent=4))

            with open("cache/joined_group.json", "r", encoding="UTF-8") as data:
                data = json.load(data)

            for i,j in data["groups"]:
                self.addScore([i,j,0,[]])
        else:
            with open("cache/score.json","r+", encoding="utf-8") as write_data:
                with open("cache/total_score.json","r") as read_data:

                    write_data_j = json.load(write_data)
                    read_data_j = json.load(read_data)

                    for j,i in enumerate(read_data_j["score"]):
                        write_data_j["score"][j][2] += i[2]
                    write_data.seek(0)
                    json.dump(write_data_j, write_data, indent = 4)

        

    
            
class makeResponse:
    def startHandler(self, message) -> str:
        self.chat_id = message.chat.id
        if not jsonManager().exist(chat_id=self.chat_id):
            group_name = name_data["names"][jsonManager().groupLen()]
            jsonManager().addGroup([self.chat_id,group_name])
            return text_data["new_start"].format(group_name)
        
        elif jsonManager().exist(chat_id=self.chat_id):
            return text_data["already_joined"]
        
    def startMessageHandler(self) -> str:
        return text_data["start_messages"]
    
    def alreadyStarted(self,chat_id) -> str:
        if jsonManager().exist(chat_id) == True:
            return text_data["game_started"]
        else:
            return text_data["already_started"]
    
    def gameStarted(self) -> str:
        return text_data["game_started"]

    def allLetterExist(self, text:str, index:int) -> bool:
        for i in text.upper():
            if i not in spelling_data["spelling"][index]:
                return False
        return True
    def final(self) -> str:
        return text_data["final_msg"]
    def messageHandler(self,chat_id:int,index:int,text:str) -> str:
        if jsonManager().exist(chat_id): 
            if not jsonManager().wordExist(chat_id, text):
                if self.allLetterExist(text,index):
                    if len(text) >= 4:
                        if jsonManager().getSpelling(index_num=index)[0] in text.upper():
                            return jsonManager().check(chat_id,text,index)
                        else: 
                            return self.centralError()
                    else:
                        return text_data["must_four"]
                else:
                    return text_data["inappropriate"]
            else:
                return text_data["scored_word"]
        else:
            return self.alreadyStarted()
    def roundChanged(self) -> str:
        return text_data["round_changed"]
    
    def centralError(self) -> str:
        return text_data["central_error"]