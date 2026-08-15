---
type: ingest-note
source: https://discourse.nixos.org/t/the-nixpkgs-core-team-has-disbanded/12345
date: 2026-08-07
tags: [nixpkgs, 治理, 开源]
---

# Nixpkgs 核心团队解散

> **来源公告**：Nixpkgs 核心团队宣布解散，全文要点整理如下。

## 事件概述

2026 年 8 月 7 日，Nixpkgs 核心团队（Nixpkgs Core Team）宣布正式解散。团队表示，虽然在过去 10 个月中取得了一系列成果，但该角色未能成为最初设想的“轻量级、兼容技术贡献”的岗位，出于健康原因，团队决定集体退出。

## 主要成果

- 改革了 committer 委派流程，并 onboarding 了 19 名新 committer
- 扩展合并机器人，赋能 maintainer
- 与 GitHub 重新建立联系，并获得赞助的 Enterprise Cloud 升级
- 协助分类 GHSA-67f2-674w-6g63，并跟踪该事件暴露的 GitHub 安全风险
- 制定了初步的自动化/AI 政策
- 帮助解决了多起升级到核心团队的突发事件

## 解散原因

团队认为，解散不可避免，主要原因包括：

- **Steering Committee（SC）缺乏委派本能**：SC 未能按照章程进行有效授权，而是对下层团队进行不必要的微观管理。
- **沟通长期不畅**：SC 成员有时不明确自己是在表达个人观点还是代表集体立场；事项被提交时往往已经带有预设处理结果；还出现越权接管团队职责的情况。
- **响应迟缓**：对团队关切的问题回应不足、延迟严重，尤其是在 GSoC、资助计划、AI 政策、版主事务和 GitHub org 所有者改革等事项上协调不力。
- **招募困难**：在招募新成员时仅有一人积极申请，外部拓展反应冷淡，团队健康循环无法维持。

## 治理反思

核心团队认为，这种局面是系统性问题，而非某个 SC 成员的个人问题。他们指出，SC 作为“代议制多数决委员会”，既未能有效充当委派的后盾，也未能成为主动决策机构。

团队推崇其内部的高信任、共识驱动决策模式，认为这比 SC 的多数投票更适合本地委派治理。他们强调，虽然社区存在深刻分歧，但自动化/AI 政策能获得不同观点人士的广泛支持，证明即使看似棘手的话题也能通过善意协商取得进展。

同时，团队也观察到，社区对治理的普遍不信任导致对抗性、零和式的分歧处理方式。这种方式虽在领导真空时可能奏效，却会让真诚参与治理的团队精疲力竭，并进一步缩小愿意参与治理的资深贡献者池子。

## 后续影响

核心团队解散恰逢 SC 选举临近。团队希望坦诚说明情况，能为未来的治理改进提供参考。Nixpkgs 项目将如何调整治理结构、填补核心团队留下的空白，仍有待观察。

## 原文摘录

> The Nixpkgs core team has unfortunately decided to [disband](https://discourse.nixos.org/t/the-nixpkgs-core-team-has-disbanded). We’re proud to have had the opportunity to lead by example in bottom‐up, consensus‐focused governance for Nixpkgs, and of our achievements over the past 10 months, including reforming the committer delegation process and onboarding 19 new committers, empowering maintainers by extending the merge bot, re‐establishing contact with GitHub and securing the sponsored Enterprise Cloud upgrade, helping triage GHSA-67f2-674w-6g63 and track the GitHub security risks exposed by that incident, and establishing an initial automation/AI policy, as well as helping resolve many incidents that were escalated to us.
>
> However, it has sadly not turned out to be the lightweight role compatible with active technical contribution that we had originally hoped it would be, and two weeks ago we reached the conclusion that stepping down is necessary for our health. We believe that it’s unsustainable for the team to continue, as demonstrated in part by our attrition to date. With only one person actively applying in response to our call for new members and mixed response to outreach, recruiting sufficiently to keep things healthy looks untenable.
>
> Therefore, especially with a Steering Committee election due imminently, we think the best way forward for Nixpkgs governance is to be honest about the circumstances that have made dissolving the team unavoidable, in the hopes that it may help future efforts.
>
> Our experience is that the Steering Committee as an institution lacks a native instinct for the delegation envisioned by the constitution, while also not being sufficiently engaged and cohesive to handle individual decisions at those levels itself. This manifests as unnecessary micromanagement of teams below them and chronically poor communication, including lack of clarity from SC members about when they’re speaking for themselves or representing a joint position, matters brought to our attention with desired outcomes already attached, taking ownership of issues entirely within delegated areas without involving relevant teams, and insufficient and delayed responses to concerns.
>
> The end result has been inadequate coordination on matters like GSoC, grants initiatives, and AI policy, slow and difficult progress on matters relevant to Nixpkgs like moderation and GitHub org owner reform, and general uncertainty about whether we are trusted to autonomously make decisions within our remit. These issues have persisted despite our repeated attempts to discuss them.
>
> This is, of course, a systemic problem rather than one any single SC member could solve; we don’t envy the demands of the role, have been impressed by the efforts of several members, and recognize that every individual naturally has limited time and energy and can only do so much in the context of a representative majoritarian committee. Ultimately, though, it leaves the SC not functioning effectively as either a representative backstop to delegation or a proactive decision‐making body.
>
> The resulting environment has acted as a consistent drag on our work, making it difficult for us to fulfil our constitutional mandate of “Project Direction, Decision-Making, Coordination with the NixOS Foundation Board, and Creation and Management of Teams, where they pertain to Nixpkgs”. We believe our high‐trust consensus decision‐making model has resulted in high‐quality discussions and good results, and is a better fit for a delegated local governance team than the majority votes used at the top level by the SC.
>
> It’s not news to anybody that our community has many strong divides and disagreements, but nonetheless we’ve seen many situations where the ability to call on the core team for a resolution has helped calm tensions and led to agreeable outcomes. We consider the strong approval for the initial automation/AI policy from people with highly divergent views to be proof that it’s possible to find paths forward and make significant improvements even on seemingly intractable topics. It inevitably takes its toll to step in under such circumstances, though.
>
> Given our own experiences and the history of the project, we understand why there is a general distrust of governance in the community, and how that has encouraged a combative, zero‐sum approach to disagreements. While those methods may work to effect change despite a leadership vacuum or to be heard by unresponsive governance, they contribute to burnout when leadership teams are trying to engage in good faith and foster productive discussion. That outcome only rewards those who don’t care to listen to the community or to pursue trust‐based consultative leadership at all, further reduces the small pool of experienced contributors with the time and desire to participate in governance, and risks locking in the historical status quo of decision‐making by deadlock and attrition.