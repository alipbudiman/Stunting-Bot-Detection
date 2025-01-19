from libs.certanty_factor.read_tabel import ReadTabel

def miz(num):
    if num < 0:
        return 0
    return num

def cf_combine(n_old, n_new):
    return n_old + n_new * (1 - n_old)

def create_cfc(num, g="other"):
    cf_pakar = 0.6
    if g == "g1":
        cf_pakar = 1.0
    elif g == "g2":
        cf_pakar = 0.8
    return num * cf_pakar

def Fungsi_Rule1(g1, g2, g4):
    cfc1 = cf_combine(create_cfc(g1, "g1"), create_cfc(g2, "g2"))
    cfc2 = cf_combine(cfc1, create_cfc(g4))
    return cfc2 * 100 

def Fungsi_Rule2(g2, g3, g4, g5):
    cfc1 = cf_combine(create_cfc(g2, "g2"), create_cfc(g3))
    cfc2 = cf_combine(cfc1, create_cfc(g4))
    cfc3 = cf_combine(cfc2, create_cfc(g5))
    return cfc3 * 100

def Fungsi_Rule3(g5, g6, g7, g8, g9):
    cfc1 = cf_combine(create_cfc(g5), create_cfc(g6))
    cfc2 = cf_combine(cfc1, create_cfc(g7))
    cfc3 = cf_combine(cfc2, create_cfc(g8))
    cfc4 = cf_combine(cfc3, create_cfc(g9))
    return cfc4 * 100

def Fungsi_Rule4(g3, g4, g6, g8, g9):
    
    cfc1 = cf_combine(create_cfc(g3), create_cfc(g4))
    cfc2 = cf_combine(cfc1, create_cfc(g6))
    cfc3 = cf_combine(cfc2, create_cfc(g8))
    cfc4 = cf_combine(cfc3, create_cfc(g9))
    return cfc4 * 100

def Fungsi_Rule5(g3, g5, g6, g8, g9):
    
    cfc1 = cf_combine(create_cfc(g3), create_cfc(g5))
    cfc2 = cf_combine(cfc1, create_cfc(g6))
    cfc3 = cf_combine(cfc2, create_cfc(g8))
    cfc4 = cf_combine(cfc3, create_cfc(g9))

    
    return cfc4 * 100


class CertantyFactor(ReadTabel):
    def __init__(self) -> None:
        super().__init__()
    
    def TransformUncertainTerm6(self, input):
        if input == "Tidak Yakin":
            return 0
        elif input == "Kurang Yakin":
            return 0.2
        elif input == "Sedikit Yakin":
            return 0.4
        elif input == "Cukup Yakin":
            return 0.6
        elif input == "Yakin":
            return 0.8
        elif input == "Sangat Yakin":
            return 1
        else:
            raise Exception("input data is not allowed!")
    
    def TransformUncertainTerm2(self, input):
        if input in ["Ya", "Tidak"]:
            if input == "Ya":return 1
            else:return 0
        else:
            raise Exception("input data is not allowed!")
            
            
    
    def Cfrule1(self, jk, age_input, height_input, weight_input, cf4):
        if jk.lower() not in ["l","p"]:
            raise Exception("jk input must l or p")
        if jk.lower() == "l":
            file_path = "rule_l.csv"
            file_path2 = "rule2_l.csv"
        if jk.lower() == "p":
            file_path = "rule_p.csv"
            file_path2 = "rule2_p.csv"
        
        rules_data = self.load_rules(file_path)
        rules_data2 = self.load_rules2(file_path2)
        
        g1 = self.stunting_status_by_age_height(age_input, height_input, rules_data)
        g2 = self.nutrition_status(height_input, weight_input, rules_data2)
        
        print("age", age_input)
        print("tinggi", height_input)
        print("berat", weight_input)
        
        res1 = Fungsi_Rule1(g1, g2, miz(cf4))
        
        return res1, g1, g2
    
    def Cfrule2(self, g2,  g3, g4, g5):
        res2 = Fungsi_Rule2(g2, miz(g4), miz(g3), miz(g5))
        
        return res2

    def Cfrule3(self, g5, g6, g7, g8, g9):
        res3 = Fungsi_Rule3(miz(g5),g6, g7, g8, g9)
        return res3
    
    def Cfrule4(self, g3, g4, g6, g8, g9):
        res4 = Fungsi_Rule4(g3, g4, miz(g6), miz(g8), miz(g9))
        return res4
        
    def Cfrule5(self, g3, g5, g6, g8, g9):
        res5 = Fungsi_Rule5(g3, g5, g6, g8, g9)
        return res5

