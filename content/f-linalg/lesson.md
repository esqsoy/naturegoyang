## 핵심 질문

파동이나 교류 전압은 크기와 함께 한 주기 중 어디쯤인지도 가진다. 갈래가 여럿인 회로는 미지수 여럿을 함께 풀어야 한다. 이를 간단히 하는 도구가 복소수와 행렬이고, 양자역학은 측정값을 이 도구로 적는다.

## 원리

### 1. 복소수의 연산과 극형식

#### 직관

단위원을 일정하게 도는 점의 가로 위치가 진동 $\cos(\omega t+\varphi)$이고($\omega=2\pi/T$, 4번), 점의 자리를 나타내는 각 $\omega t+\varphi$가 **위상**(位相, phase)이다. 가로·세로 위치를 수 하나로 묶으면 두 진동의 합은 화살표의 합, 위상을 옮기는 일은 화살표 돌리기가 된다. −1을 곱하면 반 바퀴 돌므로, 돌리기를 곱셈으로 하려면 제곱해서 −1인 90° 돌리기 $i$가 필요하다. 다만 재는 것은 가로 위치뿐이다.

#### 통상

**허수단위**(虛數單位, imaginary unit) $i$는 $i^2=-1$인 수다. 실수 $a$, $b$로 쓴 $z=a+bi$가 **복소수**(複素數, complex number), $a$가 **실수부분**(實數部分, real part), $b$가 **허수부분**(虛數部分, imaginary part)이다. **켤레복소수**(켤레複素數, complex conjugate) $\bar z=a-bi$와의 곱 $z\bar z=a^2+b^2$는 실수라서 나눗셈은 분모의 켤레를 위아래에 곱한다.

$z$를 점 $(a,b)$로 나타낸 평면이 **복소평면**(複素平面, complex plane)이다. $r=|z|=\sqrt{a^2+b^2}$이 **절댓값**(絕對값, modulus), 양의 실수축에서 시계 반대 방향으로 잰 각 θ가 **편각**(偏角, argument)이고, $z=r(\cos\theta+i\sin\theta)$가 **극형식**(極形式, polar form)이다. **오일러 공식**(Euler公式, Euler's formula) $e^{i\theta}=\cos\theta+i\sin\theta$(θ는 rad)로 $z=re^{i\theta}$라 쓰면, 곱할 때 절댓값은 곱하고 편각은 더한다. θ = π이면 $e^{i\pi}+1=0$이다.

#### 엄밀

$w=\rho(\cos\varphi+i\sin\varphi)$이면 $zw=\rho(\cos\varphi\,z+\sin\varphi\,iz)$다. $iz=-b+ai$는 $z$를 90° 돌린 점이라 괄호 안은 φ 돌린 $z$를 두 수직 방향으로 분해한 꼴(5번)이고, $zw$는 $z$를 φ 돌려 ρ배 한 점이다. $n$번 곱하면 **드무아브르의 정리**(de Moivre의定理, de Moivre's theorem) $(\cos\theta+i\sin\theta)^n=\cos n\theta+i\sin n\theta$다. 허수 지수는 지수법칙과 $(e^{kx})'=ke^{kx}$(53번)가 성립하도록 정하며, 곱하면 각이 더해지고 작은 θ(rad)에서 $\sin\theta\approx\theta$라 $1+i\theta$에 가까운 $\cos\theta+i\sin\theta$가 이를 채운다.

#### 점검
**Q.** $(1+i)(1+\sqrt3\,i)$의 절댓값과 편각은?
**A.** $\sqrt2\times2=2\sqrt2$, $45^\circ+60^\circ=105^\circ$로, 직접 곱한 $(1-\sqrt3)+(1+\sqrt3)i$와 같다.

### 2. 행렬의 곱과 연립방정식

#### 직관

연립방정식 $ax+by=p$, $cx+dy=q$에서 미지수를 떼면 계수의 표가 남는다. 이 표는 점 $(x,y)$를 $(p,q)$로 옮기는 규칙이고, 방정식 풀기는 처음 점을 거꾸로 찾는 일이다. 행렬의 곱 $AB$는 '$B$로 옮긴 뒤 $A$로 옮기기'라서, 5번의 책 돌리기처럼 순서가 결과를 바꿀 수 있다.

#### 통상

수를 직사각형으로 늘어놓은 것이 **행렬**(行列, matrix)이다. 가로줄이 **행**(行, row), 세로줄이 **열**(列, column)이고 $i$행 $j$열의 수를 성분 $a_{ij}$라 한다. 행과 열의 수가 같으면 **정사각행렬**(正四角行列, square matrix)이다. $AB$의 $(i,j)$ 성분은 $A$의 $i$행과 $B$의 $j$열을 차례로 곱해 더한 $\sum_k a_{ik}b_{kj}$이고, 일반적으로 $AB\ne BA$다.

대각선 성분이 1, 나머지가 0인 **단위행렬**(單位行列, identity matrix) $I$는 $AI=IA=A$이고, $AX=XA=I$인 $X$가 **역행렬**(逆行列, inverse matrix) $A^{-1}$이다. 2×2 행렬은 **행렬식**(行列式, determinant) $\det A=ad-bc$가 0이 아닐 때만 역행렬이 있다.

$$\begin{pmatrix}a&b\\c&d\end{pmatrix}^{-1}=\frac{1}{ad-bc}\begin{pmatrix}d&-b\\-c&a\end{pmatrix}$$

**연립일차방정식**(聯立一次方程式, system of linear equations)은 $A\vec x=\vec b$로 쓰고(벡터는 2×1 행렬), $\det A\ne0$이면 해는 $\vec x=A^{-1}\vec b$다.

#### 엄밀

$|\det A|$는 넓이의 배율이라 $\det A=0$이면 평면이 선이나 점으로 눌려 되돌릴 수 없고 해가 없거나 무수히 많다. 미지수가 많으면 식의 몇 배를 빼 미지수를 차례로 없애는 **가우스 소거법**(Gauss消去法, Gaussian elimination)을 쓴다.

#### 점검
**Q.** $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$, $B=\begin{pmatrix}1&0\\1&1\end{pmatrix}$에서 $AB$와 $BA$의 $(1,1)$ 성분은?
**A.** $1\cdot1+1\cdot1=2$와 $1\cdot1+0\cdot0=1$로 달라 $AB\ne BA$다.

### 3. 고윳값과 고유벡터

#### 직관

$A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$는 $(1,0)$을 $(2,1)$로 보내듯 대부분의 벡터 방향을 바꾼다. 그러나 직선 $y=x$ 위의 $(1,1)$은 $(3,3)$으로 방향 그대로 3배가 되고, 그 수직인 $(1,-1)$은 그대로다.

#### 통상

정사각행렬 $A$에서 $A\vec v=\lambda\vec v$인 영벡터 아닌 $\vec v$가 있으면 λ를 **고윳값**(固有값, eigenvalue), $\vec v$를 **고유벡터**(固有vector, eigenvector)라 한다. $(A-\lambda I)\vec v=\vec 0$에 영벡터 아닌 해가 있으려면 $A-\lambda I$의 역행렬이 없어야 하므로, 고윳값은 **특성방정식**(特性方程式, characteristic equation) $\det(A-\lambda I)=0$의 해다. 2×2이면 $\lambda^2-(a+d)\lambda+ad-bc=0$이다. 직관의 $A$는 $\lambda^2-4\lambda+3=0$에서 3과 1이고, 고유벡터는 각각 $(1,1)$, $(1,-1)$이다.

#### 엄밀

θ 회전 행렬 $\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$를 곱하는 것은 $x+iy$에 $e^{i\theta}$를 곱하는 것과 같다. 그 고윳값은 $e^{\pm i\theta}$라 θ가 0, π가 아니면 실수 고유벡터가 없다. $a_{ij}=a_{ji}$인 실수 행렬은 고윳값이 실수이고 다른 고윳값의 고유벡터끼리 수직이다. 72번 양자역학에서 측정값은 이를 복소수로 넓힌 행렬의 고윳값이다.

#### 점검
**Q.** $\begin{pmatrix}4&1\\2&3\end{pmatrix}$의 고윳값은?
**A.** $\lambda^2-7\lambda+10=0$에서 5와 2다.

## 예제

**예제. 회로를 역행렬로 풀기**
최혁이 위아래 두 접합점 사이에 왼쪽(16 V 전지와 2.0 Ω), 오른쪽(14 V 전지와 2.0 Ω), 가운데(4.0 Ω) 세 갈래를 이었다. 전지는 (+)극이 위, 내부 저항은 0이다.

1. 양쪽에서 위로 흐르는 전류를 $I_1$, $I_2$라 하면 가운데로는 $I_1+I_2$가 내려간다(전류 법칙). 두 고리의 전압 법칙($16=2I_1+4(I_1+I_2)$ 등)에서 $6I_1+4I_2=16$, $4I_1+6I_2=14$다.
2. 계수 행렬의 행렬식은 $36-16=20$, 역행렬은 $\frac1{20}\begin{pmatrix}6&-4\\-4&6\end{pmatrix}$이다.
3. $I_1=(6\cdot16-4\cdot14)/20=2.0$ A, $I_2=(-4\cdot16+6\cdot14)/20=1.0$ A, 가운데는 3.0 A다.

## 흔한 오개념

- **오해:** $\sqrt{-1}\sqrt{-1}=\sqrt1=1$이다. → **사실:** $a,b<0$이면 $\sqrt a\sqrt b\ne\sqrt{ab}$이고 답은 $i^2=-1$이다.
- **오해:** 영벡터도 고유벡터다. → **사실:** $A\vec 0=\lambda\vec 0$은 늘 성립해 뺀다.

## 연결

[[f-trig]]의 단위원과 [[f-vector]]의 성분 분해가 극형식의 바탕이다. 56번 진동과 공명은 진동을 $e^{i\omega t}$로 다루고, [[p-relativity]]의 로런츠 변환은 행렬이며, [[p-qm]]은 상태를 복소수로, 측정값을 고윳값으로 적는다.

## 요약

- $i^2=-1$, $z=re^{i\theta}$: 곱하면 절댓값은 곱하고 편각은 더한다. $e^{i\pi}+1=0$.
- $AB$의 $(i,j)$ 성분은 $\sum_k a_{ik}b_{kj}$, 일반적으로 $AB\ne BA$.
- $ad-bc\ne0$일 때만 $A^{-1}$이 있고 $A\vec x=\vec b$의 해는 $A^{-1}\vec b$다.
- 고윳값은 $\det(A-\lambda I)=0$의 해, 고유벡터는 늘거나 줄기만 하는 방향이다.
