---
title: "Constant reference tracking control for uncertain linear sampled-data systems"
collection: publications
category: manuscripts
permalink: /publication/2026-01-01-constant-reference-tracking
excerpt: 'This paper presents a constant reference tracking control for uncertain linear sampled-data systems.'
date: 2026-01-01
venue: 'Nonlinear Analysis: Hybrid Systems'
paperurl: 'https://doi.org/10.1016/j.nahs.2024.101651'
codeurl: '#'
citation: '<strong>Fuentes, Roberto M</strong>, Gabriel, Gabriela W, de Oliveira, André M, Palma, Jonathan M. (2026). "Constant reference tracking control for uncertain linear sampled-data systems." <i>Nonlinear Analysis: Hybrid Systems</i>. 59, 101651. DOI: 10.1016/j.nahs.2024.101651.'
---


Markdown
======
# Constant reference tracking control for uncertain linear sampled-data systems
**Roberto M. Fuentes, Jonathan M. Palma, Gabriela W. Gabriel, André M. de Oliveira** [cite: 10, 11, 12]

# Abstract
This paper studies the reference-tracking control problem for uncertain sampled-data systems with partial observation of the states. [cite: 23] We show that, by robustly stabilizing the closed-loop system, the proposed digital controller ensures that the controlled output tracks constant set points. [cite: 24] Moreover, new design conditions given in terms of Differential Linear Matrix Inequalities are presented for obtaining controllers with partial and complete measurements of the states. [cite: 25] The design conditions are illustrated by numerical examples. [cite: 26]

# 1. Introduction
A significant problem in applied engineering is the reference tracking problem, in which a system output follows a constant set point. [cite: 28] This is a traditional topic of research of control systems as illustrated by the large body of works for continuous-time systems, e.g., [1,2], and discrete-time systems [3,4], and the references therein. [cite: 29] Some techniques employed for solving control goals involving tracking are using controllers with integral action [5], model-predictive control [1], linear quadratic regulators and/or reinforcement learning [6], the use of reference generators [7], a combination of the aforementioned approaches, among others. [cite: 30] The problem of robust tracking control was also tackled in [8] for the continuous-time linear and nonlinear systems. [cite: 31]

In the past decades, control systems have been usually implemented through digital devices, and due to the effects of sampling, classical solutions could lose effectiveness in this setting, [9,10]. For instance, the performance of controllers obtained through continuous-time techniques and subsequent discretization can be degraded [11]. Another usual approach is discretizing the system and directly employing a discrete-time framework for the control design. However, in this case, inter-sampling behavior is not considered which could be critical in certain applications, e.g., [12].

In this work, we consider the problem of designing robust controllers for uncertain sampled-data systems that ensure the asymptotic stability of the closed-loop system whilst guaranteeing constant reference tracking for outputs chosen by the designer. [cite: 54]

# 2. Auxiliary results
In this section, we present some auxiliary results. [cite: 67] For that, we introduce the following general uncertain periodic impulsive system: [cite: 67]

$$\left\{\begin{matrix}\dot{\xi}(t)&=F(\alpha)\xi(t)\\ \xi(t_{k})&=H(\alpha)\xi(t_{k}^{-})+J(\alpha)r[k],\xi(t_{0}^{-})=0,\end{matrix}\right.$$ [cite: 68]

where $\xi(t)\in\mathbb{R}^{n_{\xi}}$ is the state and $r[k]\in\mathbb{R}^{n_{r}}$ is the input. [cite: 70] The impulses occur at every $t=t_{k}$, $k\in\mathbb{N},$ with fixed fundamental period $t_{k+1}-t_{k}=h>0$. [cite: 71] Similarly as in [16,25], and [26], the uncertain matrix $F(\alpha)$ is modeled by: [cite: 71]

$$F(\alpha)=\sum_{i=1}^{N}\alpha_{i}F_{i},\alpha\in A_{N}.$$ [cite: 72]

**Lemma 1.** For given $h>0$ and $r\equiv0,$ if there exists a symmetric differentiable matrix function P: [0,h) R that satisfies the following differential matrix inequalities: [cite: 76]

$$F(\alpha)^{\top}P(t)+P(t)F(\alpha)+\dot{P}(t)\le0$$ 

in the interval $t\in[0,h)$ with boundary conditions: 

$$P(0)>0, P(h)>H(\alpha)^{\top}P(0)H(\alpha)$$ 

for every $\alpha\in\Lambda_{N}$ then the system (1) is asymptotically stable. 

# 3. Problem statement
Let a linear time-invariant system be as in Fig. 1 with a uncertain time-invariant plant: 

$$\left\{\begin{matrix}\dot{x}(t)&=A(\alpha)x(t)+B(\alpha)u(t),\\ y(t)&=C_{y}(\alpha)x(t),x(0)=0,\end{matrix}\right.$$ 

where $x(t)\in\mathbb{R}^{n_{x}}$ is the state vector, $u(t)\in\mathbb{R}^{n_{u}}$ is the control input, and $y(t)\in\mathbb{R}^{n_{y}}$ is the measured output. 

The digital control structure is given by: 

$$\left\{\begin{matrix}x[k]&=x[k-1]+r[k]-\phi[k]\\ u[k]&=K_{\phi},\hat{x}[k-1]+Ky[k],\hat{x}[0]=0,\end{matrix}\right.$$ 

where $\hat{x}[k]\in\mathbb{R}^{n}\phi$ and $r[k]\in\mathbb{R}^{n_{\Phi}}$ is the set-point signal defined by: 

$$r[k]=\left\{\begin{matrix}\overline{r},k\ge0\\ 0,&otherw\end{matrix}\right. ,$$ 

for a fixed known $\overline{r}\in\mathbb{R}^{n_{\phi}}$; and the signal $\phi[k]=\phi(t_{k})$, $\phi(t)\in\mathbb{R}^{n}\phi$ is the regulated output, given by $\phi(t)=C_{\phi}y(t).$ 

# 4. Main results
This section presents the main result of tracking analysis and control. [cite: 164] In Section 4.1, we present the analysis result concerning tracking control through the controller structure (10). [cite: 165] Moreover, in Section 4.2, we present DLMI conditions to calculate the controller given in (10) for partial and complete observation of the states. [cite: 166]

**Theorem 1.** If there exists a sampling period $h>0$ and a pair (K, $K_{\phi})$ that robustly stabilizes (14), for $r[k]$ as in (11), we have that (i) $\xi(t)\rightarrow\underline{\xi_{\alpha}}$ for $t\rightarrow\alpha$ and every $\alpha\in\Lambda_{N^{j}}$ and (ii) the tracking condition (16) holds true. 

**Theorem 2.** If there exists a differentiable positive definite matrix $W(t):[0,h)\rightarrow\mathbb{R}^{n_{\xi}\times n_{\xi}}$, matrices $M\in\mathbb{R}^{n_{m}\times n_{m}}$ $U\in\mathbb{R}^{n_{y\phi}xn_{y\phi}}$ and $V\in\mathbb{R}^{n_{y\phi}xn_{u}}$ with $n_{m}=n_{x}+n_{\phi},$ $n_{y\phi}=n_{y}+n_{\phi}$ and a given scalar $\epsilon$ such that: 

$$W(t)F(\alpha)^{\top}+F(\alpha)W(t)-\dot{W}(t)\le0,$$ 

holds for all $t\in[0,h)$ and $\alpha\in\Lambda_{N}$, with the LMI conditions: 

$$\begin{bmatrix}W(h)&W(h)C_{\chi\phi}^{\top}\\ *&M\end{bmatrix}>0.$$ 

$$\begin{bmatrix}\Phi(\alpha)&\Pi_{1}(\alpha)+\epsilon\Pi_{2}^{\top}\\ *&-\epsilon(U+U^{\top})\end{bmatrix}>0$$ 

Then, by setting $\mathcal{K}^{\top}=\begin{bmatrix}K&K_{\phi}\end{bmatrix}^{\top}=U^{-1}V,$ we get the controller in (10) that stabilizes (14) and ensures that the tracking condition (16) is fulfilled. [cite: 282]