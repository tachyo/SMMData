class Search:
    base = "https://supermariomakerbookmark.nintendo.net/search/result?"
    q_template = "page={}&q%5Barea%5D={}&q%5Bcreated_at%5D={}&q%5Bdifficulty%5D={}&q%5Bscene%5D={}&q%5Bskin%5D={}&q%5Bsorting_item%5D={}&q%5Btag_id%5D=&utf8=✓"
    #themes = ["mario_bros","mario_bros3","mario_world","mario_bros_u"]
    themes = ["mario_bros_u"]
    scenes = ["ground","underground","underwater","gohst_house","castle","airship"]
    #regions = ["jp","us","eu","others"]
    regions = ["others"]
    difficultys = ["easy","normal","expert","super_expert"]
    createds = ["past_day","past_week","past_month","before_one_month"]  #currently not in use
    sortings = ["like_rate_desc","liked_count_desc","clear_rate_asc","sns_shared_count_desc","created_at_desc"]

    def __init__(self, theme='', scene='', region='', difficulty='', created='', sorting="like_rate_desc"):
        self.theme = theme
        self.scene = scene
        self.region = region
        self.difficulty = difficulty
        self.created = created
        self.sorting = sorting

    def next(self):
        currentPage = 0
        while currentPage < 100:
            currentPage += 1
            yield self.base + self.q_template.format(currentPage, self.region, self.created, self.difficulty, self.scene, self.theme, "liked_count_desc")



class ExhaustiveSearch(Search):

    def __init__(self, sorting):
        self.sorting = sorting
        self.numSearches = len(self.themes)*len(self.regions)*len(self.difficultys)*len(self.scenes)


    def next(self):
        i = 0
        for r in self.regions:
            for t in self.themes:
                for s in self.scenes:
                    for d in self.difficultys:
                        i += 1
                        print("starting search {} - {} - {} - {} ({}/{})".format(r,t,s,d,i,self.numSearches))
                        currentSearch = Search(t,s,r,d,'',self.sorting)
                        j = 0
                        for url in currentSearch.next():
                            j +=1
                            print("page {:>3}: ".format(j), end='', flush=True)
                            yield url
