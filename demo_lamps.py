#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo: عرض المصابيح المبسط في أعمدة Current State و Previous State
"""

def demo_lamp_display():
    """عرض توضيحي لكيفية عمل المصابيح"""
    
    print("🎯 عرض المصابيح المبسط - بدون أيقونات")
    print("=" * 50)
    
    # أمثلة لحالات المصابيح
    test_cases = [
        "Heat Ready",           # Heat + Ready نشط
        "Eco Clean",            # Eco + Clean نشط  
        "Heat Ready Eco Clean", # كل المصابيح نشطة
        "None",                 # لا شيء نشط
        "Heat",                 # Heat فقط نشط
        "Ready",                # Ready فقط نشط
    ]
    
    print("\n📊 أمثلة لعرض المصابيح:")
    print("-" * 30)
    
    for i, test_case in enumerate(test_cases, 1):
        if test_case == "None":
            display_text = "All OFF"
            status = "🔴"
        else:
            # تحويل النص إلى عرض المصابيح
            active_lamps = []
            lamp_names = ['Heat', 'Ready', 'Eco', 'Clean']
            
            for lamp_name in lamp_names:
                if lamp_name.lower() in test_case.lower():
                    active_lamps.append(lamp_name)
            
            if active_lamps:
                display_text = " | ".join(active_lamps)
                status = "🟢"
            else:
                display_text = "All OFF"
                status = "🔴"
        
        print(f"{i:2d}. {status} {test_case:20} → {display_text}")
    
    print("\n💡 مميزات العرض الجديد:")
    print("   ✅ نص بسيط وواضح")
    print("   ✅ بدون أيقونات معقدة")
    print("   ✅ عرض مباشر لحالة كل لمبة")
    print("   ✅ حفظ في Excel كنص مقروء")
    print("   ✅ تصميم احترافي ومتسق")
    
    print("\n📁 عند الحفظ في Excel:")
    print("   - Current State: Heat | Ready")
    print("   - Previous State: All OFF")
    print("   - يمكن قراءة البيانات بسهولة")
    print("   - مناسب للتقارير والتحليل")

if __name__ == "__main__":
    demo_lamp_display()
