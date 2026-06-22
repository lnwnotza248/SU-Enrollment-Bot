from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime

# ==================== จุดประสงค์และคำเตือนก่อนใช้งานโปรแกรม ====================
print("==========================================================================")
print("🤖 [SU Enrollment Bot]")
print("==========================================================================")
print("📌 จุดประสงค์ของโปรแกรม:")
print("  โปรแกรมนี้ถูกพัฒนาขึ้นมาเพื่อเป็น 'โปรเจกต์ทดลองเล่น ๆ' สำหรับศึกษากระบวนการทำงาน")
print("  ของระบบ Web Automation ด้วย Selenium เท่านั้น ผู้พัฒนาไม่ได้มีเจตนาทุจริตใด ๆ ทั้งสิ้น")
print("")
print("🚨 DISCLAIMER (คำปฏิเสธความรับผิดชอบ):")
print("  ผู้พัฒนาจะไม่รับผิดชอบต่อความเสียหายใด ๆ ที่เกิดขึ้นจากการนำบอทนี้ไปใช้งานในทุกกรณี!")
print("  (ไม่ว่าจะเป็นการลงทะเบียนผิดพลาด, วิชาหาย, ระบบล็อก หรือถูกลงโทษตามกฎของมหาวิทยาลัย)")
print("  ผู้ใช้ต้องยอมรับความเสี่ยงด้วยตัวเองทั้งหมด!")
print("==========================================================================")
print("🛑 [คำเตือนสำคัญมากจากประสบการณ์ตรงของผู้สร้าง - PLEASE READ] 🛑")
print("==========================================================================")
print("⚠️ WARNING 1: เมื่อคุณกรอกรหัสผ่านเสร็จ บอทจะเริ่มทำงานและกดยืนยันลงทะเบียนทันที")
print("  คุณจะไม่สามารถแก้ไขหรือยกเลิกได้ หากต้องการแก้ไข ต้องรอช่วงเพิ่ม-ถอนเท่านั้น")
print("")
print("⚠️ WARNING 2: ระวัง Bugs 'การลงทะเบียนไม่อยู่ในเวลา' (สตอรี่ความ fail ของคนทำแอป 555)")
print("  หากถึงเวลาลงทะเบียนแล้ว (08:30 น.) แต่บอทเอาแต่วนลูปรีเฟรช")
print("  ❌ สาเหตุหลัก: เป็นเพราะในวิชาที่คุณเลือกมีวิชาพิเศษบางวิชา (เช่น SU402) ที่ล็อกเงื่อนไขไว้เฉพาะคณะอื่นเท่านั้น")
print("    มันจึงขึ้นว่า 'ไม่ได้อยู่ในช่วงลงทะเบียน'")
print("    คนทำแอปเคย fail มาแล้วเพราะวิชานี้ บอทค้างไม่ยอมกดให้")
print("    จนต้องไปกดถอนวิชา SU402 ออก และถอนวิชาที่อยากเรียนออกไปตัวหนึ่งเพื่อลองระบบ")
print("    แต่ดันลืมปิดบอท ผลคือบอทมันรันต่ออัตโนมัติแล้วกดลงทะเบียนทันที!")
print("    สรุปคือวิชาที่อยากเรียนจริงๆ ก็ไม่ได้เรียน ต้องไปรอช่วงเพิ่ม-ถอน เซ็ง")
print("  💡 คำแนะนำ: อย่าเพิ่งเลือกวิชาเจ้าปัญหาเหล่านี้ ค่อยไปเพิ่มช่วงเพิ่ม-ถอนแทน!")
print("")
print("⚠️ WARNING 3: หากมีวิชาใดวิชาหนึ่งที่คุณเลือกไว้เกิดเต็ม")
print("  บอทจะไม่สามารถกดยืนยันลงทะเบียนให้สำเร็จได้ เนื่องจากระบบเว็บของ ม. จะบล็อกไม่ให้ผ่าน")
print("")
print("📌 RECOMMENDATION :")
print("  1. แนะนำให้เลือก 'เฉพาะวิชาที่คิดว่าจะเต็มเร็ว/แย่งกันสูง'")
print("     แล้วสั่งรันบอทนี้เพื่อยืนยันวิชาเหล่านั้นมาก่อนให้ได้เป็นอันดับแรก")
print("  2. ส่วนวิชาอื่น ๆ ที่เหลือ (วิชาทั่วไปที่โควตาเยอะ หรือวิชาทุกคณะเรียนรวมกัน) ปล่อยผ่านไปก่อน")
print("     ค่อยไปเพิ่มช่วงเพิ่ม-ถอนรายวิชาแทน จะปลอดภัยที่สุด!")
print("==========================================================================")
print("")

# บังคับพิมพ์ OK เพียงครั้งเดียวหลังจากอ่านความละเอียดทั้งหมด
while True:
    confirm_all = input("👉 พิมพ์ 'OK' (ตัวพิมพ์ใหญ่) เพื่อยืนยันว่าเข้าใจและยอมรับความเสี่ยงทั้งหมด: ").strip()
    if confirm_all == "OK":
        print("==========================================================================")
        break
    else:
        print("❌ กรุณาพิมพ์ 'OK' เพื่อดำเนินการต่อ ")
# ==================== ตั้งค่าข้อมูลของคุณตรงนี้ ====================
print("🔒 กรุณากรอกข้อมูลเข้าสู่ระบบ (ข้อมูลนี้จะไม่ถูกบันทึกไว้ที่ใดทั้งสิ้น)")
USERNAME = input("👤 รหัสประจำตัวนักศึกษา: ")
PASSWORD = input("🔑 รหัสผ่าน: ")
# ============================================================

# ==================== ฟังก์ชันตั้งเวลาทำงานล่วงหน้า ====================
print("\n⏰ [ระบบตั้งเวลาเริ่มทำงานล่วงหน้า]")
target_time_str = ""

# วนลูปเช็คว่าผู้ใช้พิมพ์แค่ Y หรือ N เท่านั้น
while True:
    is_scheduled = input("👉 คุณต้องการตั้งเวลาให้บอทเริ่มทำงานล่วงหน้าหรือไม่? ถ้า N บอทจะทำงานทันที (Y/N): ").strip().upper()
    if is_scheduled in ["Y", "N"]:
        break
    else:
        print("❌ กรุณาพิมพ์ตอบแค่ Y หรือ N เท่านั้น! (ตัวพิมพ์เล็กหรือใหญ่ก็ได้)")

if is_scheduled == "Y":
    while True:
        target_time_str = input("⏰ ระบุเวลาที่ต้องการให้บอทเริ่มทำงาน (รูปแบบ HH:MM:SS เช่น 08:29:50): ").strip()
        try:
            # ตรวจสอบรูปแบบเวลาว่าถูกต้องไหม
            datetime.strptime(target_time_str, "%H:%M:%S")
            print(f"🎯 ตั้งเวลาบอทเรียบร้อย! ระบบจะสแตนด์บายจนถึงเวลา {target_time_str} น.")
            break
        except ValueError:
            print("❌ รูปแบบเวลาไม่ถูกต้อง! กรุณากรอกในรูปแบบ HH:MM:SS (เช่น 08:29:50)")
else:
    print("🚀 ไม่ตั้งเวลาล่วงหน้า -> ระบบจะเริ่มทำงานทันที!")

print("\n⏳ รอสักครู่...")
# ============================================================

BASE_URL = "https://reg4.su.ac.th"
LOGIN_URL = f"{BASE_URL}/registrar/login"
ENROLL_URL = f"{BASE_URL}/registrar/enroll"

# ==================== ลูปนับถอยหลังรอเวลา (ถ้ามีการตั้งเวลา) ====================
if is_scheduled == "Y" and target_time_str != "":
    print("⏳ บอทกำลังอยู่ในโหมด Standby...")
    while True:
        current_now = datetime.now().strftime("%H:%M:%S")
        if current_now >= target_time_str:
            print(f"⏰ [ALERT] ถึงเวลา {current_now} น. แล้ว! เริ่มเดินเครื่องบอททันที!")
            break
        time.sleep(0.5)  # เช็คเวลาทุก ๆ 0.5 วินาที เพื่อความแม่นยำและไม่เปลือง CPU

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--blink-settings=imagesEnabled=false')  # ปิดรูปภาพเพื่อความเร็วสูงสุด
    options.add_argument('--disable-notifications')               # ปิดแจ้งเตือนกวนใจ
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

def login(driver):
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver, 15)
    print("🔄 กำลังเปิดหน้า Login...")
    
    username_field = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[type='text'][placeholder='รหัสประจำตัว']")
    ))
    username_field.clear()
    username_field.send_keys(USERNAME)

    password_field = driver.find_element(
        By.CSS_SELECTOR, "input[type='password'][placeholder='รหัสผ่าน']"
    )
    password_field.clear()
    password_field.send_keys(PASSWORD)

    login_btn = driver.find_element(
        By.XPATH, "//button[.//span[contains(text(),'เข้าสู่ระบบ')]]"
    )
    login_btn.click()
    
    wait.until(EC.url_changes(LOGIN_URL))
    print("✅ Login สำเร็จเรียบร้อย!")

def try_enroll(driver):
    wait = WebDriverWait(driver, 1)
    driver.get(ENROLL_URL)
    
    # -------------------------------------------------------------
    # สเต็ปที่ 1: บังคับกดปุ่ม "ยอมรับเงื่อนไข" (ปุ่มสีเขียวธรรมดา)
    # -------------------------------------------------------------
    try:
        accept_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'btn-success') and .//span[contains(text(), 'ยอมรับเงื่อนไข')]]")
        ))
        driver.execute_script("arguments[0].click();", accept_btn)
        print("☑️ [STEP 1] กดปุ่ม 'ยอมรับเงื่อนไข' สำเร็จ!")
        time.sleep(0.1) # หน่วงสั้นมากๆ ให้ระบบตื่นตัว
    except Exception as e:
        print(f"⏳ [{datetime.now().strftime('%H:%M:%S')}] ยังกดปุ่มยอมรับไม่ได้ (ระบบยังไม่เปิด)... กำลังรีเฟรช")
        return False

    # -------------------------------------------------------------
    # สเต็ปที่ 2: กดปุ่ม "ตรวจสอบ" (ปุ่มไล่เฉดสี ตัวที่ 1) - แก้ไขพิมพ์ผิดแล้ว!
    # -------------------------------------------------------------
    print("🚀 [STEP 2] กำลังกดปุ่ม 'ตรวจสอบ' อัตโนมัติ...")
    xpath_check_btn = "//button[contains(@class, 'btn-gradient-success') and .//span[contains(text(), 'ตรวจสอบ')]]"
    
    try:
        check_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_check_btn)))
        driver.execute_script("arguments[0].click();", check_btn)
        print("⚡ [STEP 2] กดปุ่ม 'ตรวจสอบ' สำเร็จ!")
        time.sleep(0.1) # หน่วงสั้นๆ รอระบบ Angular เรนเดอร์ปุ่มถัดไปโผล่ขึ้นมา
    except Exception as e:
        print("⚠️ ติดปัญหาที่สเต็ปปุ่มตรวจสอบ (หน้าเว็บอาจโหลดไม่ทัน) -> รีเซ็ทรันใหม่")
        return False

    # -------------------------------------------------------------
    # สเต็ปที่ 3: กดปุ่ม "ยืนยันลงทะเบียน" (ปุ่มไล่เฉดสี ตัวสุดท้ายที่น็อตเพิ่งเจอ!)
    # -------------------------------------------------------------
    print("🔥 [STEP 3] ตีป้อมสุดท้าย! กำลังกดปุ่ม 'ยืนยันลงทะเบียน'...")
    xpath_confirm_btn = "//button[contains(@class, 'btn-gradient-success') and .//span[contains(text(), 'ยืนยันลงทะเบียน')]]"
    
    # วนลูปย้ำปุ่มยืนยัน 5 ครั้งเพื่อความชัวร์ เผื่อเซิร์ฟเวอร์หน่วง
    for attempt in range(5):
        try:
            confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_confirm_btn)))
            driver.execute_script("arguments[0].click();", confirm_btn)
            print("🏆🏆🏆 [SUCCESS] กดปุ่ม 'ยืนยันลงทะเบียน' สำเร็จเรียบร้อย!! วิชาเป็นของเราแล้ว! 🏆🏆🏆")
            return True # หลุดลูปใหญ่ หยุดรีเฟรชหน้าเว็บทันที ชนะ!
        except Exception as e:
            print(f"🔄 กำลังย้ำปุ่มยืนยันลงทะเบียน... (รอบที่ {attempt+1})")
            time.sleep(0.1)
            
    return False

# ========== เริ่มต้นระบบสแตนด์บายแย่งชิง ==========
driver = setup_driver()

try:
    login(driver)
    print("🚀 เริ่มบอทรอเวลาลงทะเบียนเรียน...")
    
    loop_count = 1
    while True:
        is_success = try_enroll(driver)
        
        # ถ้าคอมโบสำเร็จครบทุกปุ่ม (True) ให้สั่งหลุดลูปหยุดรีเฟรชทันที
        if is_success:
            print("🛑 [STOP LOOP] ภารกิจสำเร็จ! หยุดระบบวนลูปรีเฟรชอัตโนมัติแล้ว")
            break
            
        # หน่วงเวลา 1 วินาทีก่อนเปิดหน้าเว็บเพื่อเช็กใหม่ในรอบถัดไป
        loop_count += 1
        time.sleep(1) 

    input("🎉 บอทเคลียร์คอมโบ 1-2-3 และหยุดลูปให้เรียบร้อยแล้ว! เช็กหน้าต่างเบราว์เซอร์ แล้วกด Enter เพื่อปิดโปรแกรม...")

except Exception as e:
    print(f"\n❌ [LOOP BROKEN] บอทหยุดวนลูปเนื่องจากเกิดข้อผิดพลาดฉุกเฉิน: {e}")
    print("--------------------------------------------------")
    input("👉 เกิดข้อผิดพลาด! กด Enter ตรงนี้เพื่อปิดโปรแกรม...")

finally:
    print("🔚 สิ้นสุดกระบวนการทำงาน บราว์เซอร์จะเปิดค้างไว้ให้คุณตรวจสอบผลลัพธ์")