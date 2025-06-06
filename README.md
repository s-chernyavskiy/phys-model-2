Моделирование №2. "Призма"
=
Лунная Призма, дай мне силу!
-

Во время исследования физической зависимости показателя преломления частоты от частоты, происходит совокупность явлений.
В физике такие явления принято называть **дисперсией света**. 

Один из самых наглядных примеров дисперсии — разложение белого света при прохождении его через призму. Данное явление
наблюдал еще Исаак Ньютон около 1672 года, хотя наука смогла теоретически объяснить это явление значительно позднее.

Тем не менее, именно это явление и было смоделировано, для призм различных форм.

Основные законы и формулы, используемые для расчёта
-

- Свет преломляется по закону Снелла:
    
    $n_1(\hat{\mathbf{i}} \times \hat{\mathbf{n}}) = n_2(\hat{\mathbf{t}} \times \hat{\mathbf{n}})$, где:
    - $\hat{\mathbf{i}}$ - единичный вектор падающего луча

    - $\hat{\mathbf{t}}$ - единичный вектор преломленного луча

    - $\hat{\mathbf{n}}$ - единичный вектор нормали к поверхности

    - $n_1$, $n_2$ - показатели преломления сред
- Расчет преломленного луча:

    $\cos\theta_i = -\hat{\mathbf{i}} \cdot \hat{\mathbf{n}}$
    
    $n = \frac{n_1}{n_2(\lambda)}$
    
    $\sin^2\theta_t = n^2(1 - \cos^2\theta_i)$
    
    $\cos\theta_t = \sqrt{1 - \sin^2\theta_t} \quad \text{(при отсутствии полного внутреннего отражения)}$
    
    $\hat{\mathbf{t}} = n\hat{\mathbf{i}} + (n\cos\theta_i - \cos\theta_t)\hat{\mathbf{n}}$
- Условие полного внутреннего отражения:
    $\sin^2\theta_t > 1 \quad \implies \quad \text{преломление невозможно}$
- Закон отражения:

    $\hat{\mathbf{r}} = \hat{\mathbf{i}} - 2(\hat{\mathbf{i}} \cdot \hat{\mathbf{n}})\hat{\mathbf{n}}$, где
    
    $\hat{\mathbf{r}}$ - единичный вектор отраженного луча
- Расчет нормали к поверхности для пространства $[dx, dy]$ между точками $P_1(x_1,y_1)$ и $P_2(x_2,y_2)$:

    $dx = x_2 - x_1, \quad dy = y_2 - y_1$
    
    $\hat{\mathbf{n}} = \left( \frac{dy}{\sqrt{dx^2 + dy^2}}, -\frac{dx}{\sqrt{dx^2 + dy^2}} \right)$
- Определение направления нормали:
    
    $\text{Если} \quad \hat{\mathbf{i}} \cdot \hat{\mathbf{n}} > 0 \quad \text{то} \quad \hat{\mathbf{n}} \leftarrow -\hat{\mathbf{n}}, \quad n_1 \leftrightarrow n_2$

- Пересечение прямых

  - Параметрическое уравнение для луча:
      $\mathbf{r}(t) = \mathbf{s} + t\hat{\mathbf{d}}, \quad t > 0$
  - Уравнение для участка поверхности:
      $\mathbf{p}(u) = \mathbf{a} + u(\mathbf{b} - \mathbf{a}), \quad 0 \leq u \leq 1$
  - Решаем систему:

    $t = \frac{(\mathbf{a} - \mathbf{s}) \times (\mathbf{b} - \mathbf{a})}{\hat{\mathbf{d}} \times (\mathbf{b} - \mathbf{a})}, \quad u = \frac{(\mathbf{s} - \mathbf{a}) \times \hat{\mathbf{d}}}{\hat{\mathbf{d}} \times (\mathbf{b} - \mathbf{a})}$
- Преобразование волны в цвет:

$h = \frac{2000 - \lambda}{1900} \times 0.75 \quad (0 \leq h < 1)$

$H' = 6h$

$\quad (r,g,b) = \begin{cases} 
(1, H'-\lfloor H'\rfloor, 0) & \lfloor H'\rfloor \mod 6 = 0 \\
(1-(H'-\lfloor H'\rfloor), 1, 0) & \lfloor H'\rfloor \mod 6 = 1 \\
(0, 1, H'-\lfloor H'\rfloor) & \lfloor H'\rfloor \mod 6 = 2 \\
(0, 1-(H'-\lfloor H'\rfloor), 1) & \lfloor H'\rfloor \mod 6 = 3 \\
(H'-\lfloor H'\rfloor, 0, 1) & \lfloor H'\rfloor \mod 6 = 4 \\
(1, 0, 1-(H'-\lfloor H'\rfloor)) & \lfloor H'\rfloor \mod 6 = 5 
\end{cases}$

Запуск
-
1) Установить библиотеки в `requirements.txt`
2) Запустить `main.py`:
    ```bash
    python3 main.py
    ```
3) Наслаждаться визуализацией!


Вывод
-
Было построена дисперсионная картина, работающая с разнофигурными призмами. Также, можно менять угол треугольной призмы,
смотреть на ход дисперсии, а можно в частном порядке смотреть на ход той или иной волны.
Помимо этого, можно успешно посмотреть, как будет меняться ход волны взависимости от материала, среды. 