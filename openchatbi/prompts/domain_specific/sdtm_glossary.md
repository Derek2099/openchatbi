# CDISC SDTM IG 3.4 业务术语表

## 组织信息
- **领域**: Clinical Trial Data Management（临床试验数据管理）
- **标准**: CDISC SDTM (Study Data Tabulation Model) Implementation Guide Version 3.4
- **目的**: 标准化临床试验数据收集、交换和监管提交

---

## 核心概念

### 研究相关术语

| 术语 | 英文 | 定义 | SDTM 变量 |
|------|------|------|-----------|
| 研究 | Study | 一项完整的临床试验 | STUDYID |
| 受试者 | Subject | 参与临床试验的个体 | USUBJID, SUBJID |
| 研究中心 | Site | 开展临床试验的医疗机构 | SITEID |
| 访视 | Visit | 受试者的研究相关就诊 | VISIT, VISITNUM |
| 治疗组 | Arm/Treatment Group | 受试者分配的治疗方案组 | ARM, ARMCD |

### 人口统计学术语

| 术语 | 英文 | 定义 | SDTM 域 | 变量 |
|------|------|------|---------|------|
| 年龄 | Age | 受试者年龄 | DM | AGE, AGEU |
| 性别 | Sex | 生理性别 | DM | SEX |
| 种族 | Race | 种族分类 | DM | RACE |
| 民族 | Ethnicity | 民族/族裔 | DM | ETHNIC |
| 国家 | Country | 受试者所在国家 | DM | COUNTRY |

### 不良事件术语

| 术语 | 英文 | 定义 | SDTM 域 | 变量 |
|------|------|------|---------|------|
| 不良事件 | Adverse Event (AE) | 受试者出现的任何不良医学事件 | AE | AETERM, AEDECOD |
| 严重不良事件 | Serious Adverse Event (SAE) | 导致死亡、危及生命等的严重事件 | AE | AESER |
| 严重程度 | Severity | AE 的严重程度等级 | AE | AESEV |
| 因果关系 | Causality/Relationship | AE 与研究药物的因果关系 | AE | AEREL |
| AE 结局 | Outcome | 不良事件的最终结局 | AE | AEOUT |
| AE 开始日期 | Start Date | 不良事件开始的日期 | AE | AESTDTC |
| AE 结束日期 | End Date | 不良事件结束的日期 | AE | AEENDTC |

### 生命体征术语

| 术语 | 英文 | 定义 | SDTM 域 | 变量 |
|------|------|------|---------|------|
| 生命体征 | Vital Signs | 基本生理指标测量 | VS | VSTESTCD, VSTEST |
| 收缩压 | Systolic Blood Pressure | 收缩压测量值 | VS | VSTESTCD='SYSBP' |
| 舒张压 | Diastolic Blood Pressure | 舒张压测量值 | VS | VSTESTCD='DIABP' |
| 脉搏 | Pulse Rate | 脉搏/心率 | VS | VSTESTCD='PULSE' |
| 体温 | Temperature | 体温测量值 | VS | VSTESTCD='TEMP' |
| 体重 | Weight | 体重测量值 | VS | VSTESTCD='WEIGHT' |
| 身高 | Height | 身高测量值 | VS | VSTESTCD='HEIGHT' |

### 实验室检查术语

| 术语 | 英文 | 定义 | SDTM 域 | 变量 |
|------|------|------|---------|------|
| 实验室检查 | Laboratory Test | 血液、尿液等实验室检测 | LB | LBTESTCD, LBTEST |
| 检查结果 | Test Result | 实验室检查的原始结果 | LB | LBORRES |
| 标准化结果 | Standardized Result | 标准化后的数值结果 | LB | LBSTRESN |
| 单位 | Unit | 检查结果的单位 | LB | LBORRESU, LBSTRESU |
| 正常值范围 | Normal Range | 正常参考值范围 | LB | LBSTNRLO, LBSTNRHI |
| 正常值标志 | Normal Range Indicator | 结果是否在正常范围内 | LB | LBNRIND |

### 用药记录术语

| 术语 | 英文 | 定义 | SDTM 域 | 变量 |
|------|------|------|---------|------|
| 伴随用药 | Concomitant Medication | 研究期间使用的其他药物 | CM | CMTRT, CMDECOD |
| 暴露 | Exposure | 研究药物暴露记录 | EX | EXTRT, EXDOSE |
| 剂量 | Dose | 药物剂量 | EX | EXDOSE, EXDOSU |
| 给药途径 | Route of Administration | 药物给药方式 | EX | EXROUTE |
| 给药频率 | Dosing Frequency | 给药频率 | EX | EXDOSFRQ |

---

## SDTM 核心变量说明

### 通用标识符变量

- **STUDYID**: 研究唯一标识符
- **DOMAIN**: 域代码（DM, AE, VS, LB 等）
- **USUBJID**: 受试者唯一标识符（格式: STUDYID-SITEID-SUBJID）
- **SUBJID**: 受试者在研究中心内的 ID

### 时间相关变量

- **--STDTC**: 事件/观察开始日期时间（ISO 8601 格式）
- **--ENDTC**: 事件/观察结束日期时间
- **RFSTDTC**: 首次研究治疗日期
- **RFENDTC**: 最后研究治疗日期

### 结果变量

- **--ORRES**: 原始结果（字符型）
- **--ORRESU**: 原始结果单位
- **--STRESC**: 标准化结果（字符型）
- **--STRESN**: 标准化结果（数值型）
- **--STRESU**: 标准化结果单位

### 分类变量

- **--TESTCD**: 测试/参数短代码
- **--TEST**: 测试/参数名称
- **--CAT**: 类别
- **--SCAT**: 子类别

---

## 常用指标定义

### 安全性指标

| 指标 | 定义 | 计算方法 |
|------|------|----------|
| AE 发生率 | 发生至少一次 AE 的受试者比例 | (发生AE的受试者数 / 总受试者数) × 100% |
| SAE 发生率 | 发生至少一次 SAE 的受试者比例 | (发生SAE的受试者数 / 总受试者数) × 100% |
| 药物相关 AE 率 | 与研究药物相关的 AE 比例 | (相关AE数 / 总AE数) × 100% |
| 因 AE 退出率 | 因 AE 退出研究的受试者比例 | (因AE退出人数 / 总受试者数) × 100% |

### 人口统计学指标

| 指标 | 定义 | 来源 |
|------|------|------|
| 入组受试者数 | 签署知情同意书的受试者总数 | DM 域 |
| 完成研究人数 | 完成所有研究访视的受试者数 | DS 域 |
| 平均年龄 | 受试者年龄的算术平均值 | DM.AGE |
| 性别分布 | 男性/女性受试者的比例 | DM.SEX |

### 疗效指标（示例）

| 指标 | 定义 | 来源 |
|------|------|------|
| 应答率 | 达到预定义疗效标准的受试者比例 | RS 域 |
| 疾病进展时间 | 从治疗开始到疾病进展的时间 | TU, RS 域 |

---

## 数据关系

### 主要关联键

```
DM (Demographics)
  └─ USUBJID ─┬─ AE (Adverse Events)
              ├─ VS (Vital Signs)
              ├─ LB (Laboratory)
              ├─ EX (Exposure)
              ├─ CM (Concomitant Meds)
              ├─ MH (Medical History)
              └─ DS (Disposition)
```

所有域表通过 **USUBJID** 关联到受试者的人口统计学信息（DM 域）。

---

## 常用业务问题模板

### 安全性分析
- "有多少受试者出现了严重不良事件？"
- "各治疗组的 AE 发生率是多少？"
- "显示所有药物相关的不良事件"
- "哪些受试者因不良事件退出了研究？"

### 人口统计学分析
- "受试者的平均年龄是多少？"
- "各治疗组的性别分布如何？"
- "有多少受试者来自亚洲？"
- "年龄大于 65 岁的受试者有多少？"

### 生命体征分析
- "显示基线和治疗后的血压变化"
- "哪些受试者的收缩压超过 140 mmHg？"
- "各访视的平均体重变化趋势"

### 实验室检查分析
- "显示肝功能异常的受试者"
- "ALT 值超过正常值上限 3 倍的病例"
- "各组的血红蛋白平均值对比"

---

## 别名和同义词

### 中英文对照
- 受试者 = Subject = Patient（在临床试验中通常用 Subject）
- 不良事件 = AE = Adverse Event
- 严重不良事件 = SAE = Serious Adverse Event
- 治疗组 = Arm = Treatment Group
- 安慰剂 = Placebo = 对照组

### 常用缩写
- DM: Demographics（人口统计学）
- AE: Adverse Events（不良事件）
- VS: Vital Signs（生命体征）
- LB: Laboratory（实验室检查）
- EX: Exposure（暴露/用药）
- CM: Concomitant Medications（伴随用药）
- MH: Medical History（病史）
- DS: Disposition（处置）
- SV: Subject Visits（受试者访视）

---

## 数据质量规则

### CDISC 命名约定
- 变量名使用大写字母
- 域代码为 2 个字符（DM, AE 等）
- 测试代码（--TESTCD）最多 8 个字符
- 日期时间使用 ISO 8601 格式（YYYY-MM-DDTHH:MM:SS）

### 必需变量
- 所有域必须有: STUDYID, DOMAIN, USUBJID
- 事件域必须有: --SEQ（序列号）
- 发现域必须有: --TESTCD, --TEST

### 数据完整性
- USUBJID 必须在 DM 域中存在
- --STDTC 不能晚于 --ENDTC
- 数值结果（--STRESN）必须与单位（--STRESU）匹配

---

此术语表应作为所有 SDTM 相关提示词的基础参考文档。
