from service.Paillier import PaillierEncryptor
from sqlalchemy import create_engine
import pandas as pd
from service.analyse import AnalyseService  # 导入AnalyseService

# 初始化Paillier加密器
encryptor = PaillierEncryptor()

# 创建数据库连接
engine = create_engine('mysql://root:123456@localhost/keshe')

# 读取shuju2表的所有内容
df = pd.read_sql('shuju2', con=engine)

# 解密age列的第一个数据
ciphertext = df['age'].iloc[-1]  # 获取age列的第一个密文数据
#a = 2799544581267740017272556484372051383467243418736775723879950282081233351345522330478187105235733664006957772331862939105616451634976935690993921145609384790830266665977366950070261821787169541445340844095115973322771033964870259163765084090649575824756194582098448251025876883195436484690334127278624892738527278383317820995067059288847617379608013031686603435446305577320581333535160647100335085289114204386421870619131544281563940908145386957912804497233416396167428432020417784048856042614613290198051867295940727569831825395313502789001608977762994146430338495123152702924996704857359738477753939000566424423447
encrypted_number = encryptor.public_key.encrypt(0).__class__(encryptor.public_key, int(ciphertext))  # 将密文转换为EncryptedNumber对象
decrypted_value = encryptor.decrypt(encrypted_number)  # 使用私钥解密数据

# 打印解密结果
print("age列的第一个数据的解密结果:", decrypted_value)

# # 读取shuju表的所有内容
# df = pd.read_sql('shuju', con=engine)
# # 加密所有数据（除了id列）
# for col in df.columns:
#     if col != 'id':  # 跳过id列
#         df[col] = df[col].apply(lambda x: str(encryptor.encrypt(x).ciphertext()))

# # 将加密后的数据存入shuju2表
# df.to_sql('shuju2', con=engine, if_exists='replace', index=False)
# print("加密数据已成功存入shuju2表")