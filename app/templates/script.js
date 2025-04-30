        let isFamilyFormVisible = false;
        let isFormVisible = false;
        let financeChart = null;
        let isPurchaseFormVisible = false;

        function toggleAddPurchaseForm() {
            const form = document.getElementById('addPurchaseForm');
            isPurchaseFormVisible = !isPurchaseFormVisible;
            form.style.display = isPurchaseFormVisible ? 'block' : 'none';
        }


        async function loadFamilies() {
            try {
                const response = await fetch('http://localhost:8000/families');
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                const families = await response.json();

                const select = document.getElementById('familySelect');
                select.innerHTML = '<option value="">Выберите семью...</option>';
                families.forEach(family => {
                    const option = document.createElement('option');
                    option.value = family.group_name;
                    option.textContent = family.group_name;
                    select.appendChild(option);
                });
                document.getElementById('totalFamilies').textContent = families.length;
            } catch (error) {
                console.error('Ошибка загрузки:', error);
                alert('Ошибка загрузки данных. Проверьте консоль.');
            }
        }
        window.onload = async () => {
            await loadFamilies();
            document.getElementById('totalFamilies').textContent =
                    document.getElementById('familySelect').options.length - 1;
        };

            async function loadFamilyData(familyName) {
                if (!familyName) {
                    document.getElementById('familyInfo').style.display = 'none';
                    return;
                }

                try {
                    const response = await fetch(`http://localhost:8000/families/search/?group_name=${familyName}`);
                    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                    const familyData = await response.json();

                    const userSelect = document.getElementById('purchaseUser');
                    userSelect.innerHTML = familyData.users.map(user =>
                            `<option value="${user.id}">${user.name} ${user.surname}</option>`
                    ).join('')


                document.getElementById('createdAt').textContent = familyData.created_at;
                document.getElementById('totalBalance').textContent =
                    `${familyData.total_balance.toLocaleString()} ₽`;
                document.getElementById('lastActivity').textContent =
                    new Date().toLocaleDateString('ru-RU');


                document.getElementById('membersCount').textContent = familyData.users_count;
                document.getElementById('totalExpenditure').textContent =
                    `${familyData.expenditure.toLocaleString()} ₽`;


                const usersList = document.getElementById('usersList');
                usersList.innerHTML = familyData.users.map(user => `
                    <div class="d-flex align-items-center gap-3 p-2 bg-light rounded">
                        <div class="user-avatar">
                            ${user.name[0]}${user.surname[0]}
                        </div>
                        <div>
                            <div class="fw-bold">${user.name} ${user.surname}</div>
                            <small class="text-muted">${user.email}</small>
                        </div>
                    </div>
                `).join('');


                const purchasesList = document.getElementById('purchasesList');
                purchasesList.innerHTML = familyData.purchases.map(purchase => `
                    <div class="purchase-item">
                        <div>
                            <div class="fw-bold">${purchase.description}</div>
                            <small class="text-muted">${purchase.user_name}</small>
                        </div>
                        <div class="text-success fw-bold">
                            ${purchase.price.toLocaleString()} ₽
                        </div>
                    </div>
                `).join('');

                if (financeChart) financeChart.destroy();
                const ctx = document.getElementById('financeChart').getContext('2d');
                financeChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Доходы', 'Расходы'],
                        datasets: [{
                            data: [familyData.income, familyData.expenditure],
                            backgroundColor: ['#2ecc71', '#e74c3c']
                        }]
                    }
                });

                document.getElementById('familyInfo').style.display = 'flex';
            } catch (error) {
                console.error('Ошибка загрузки:', error);
                alert('Ошибка загрузки данных семьи');
            }
        }

        const userSelect = document.getElementById('purchaseUser');
        userSelect.innerHTML = familyData.users.map(user =>
                `<option value="${user.id}">${user.name} ${user.surname}</option>`
        ).join('');


        async function addNewPurchase() {
            const familyName = document.getElementById('familySelect').value;
            const newPurchase = {
                price: parseFloat(document.getElementById('purchasePrice').value),
                description: document.getElementById('purchaseDesc').value,
                user_id: document.getElementById('purchaseUser').value
            };

            try {
                const response = await fetch(`/families/${familyName}/purchases`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(newPurchase)
                });

                if (!response.ok) throw new Error(await response.text());


                document.getElementById('purchasePrice').value = '';
                document.getElementById('purchaseDesc').value = '';
                await loadFamilyData(familyName);
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Ошибка при добавлении покупки: ' + error.message);
            }
        }

        function toggleAddFamilyForm() {
            const form = document.getElementById('addFamilyForm');
            isFamilyFormVisible = !isFamilyFormVisible;
            form.style.display = isFamilyFormVisible ? 'block' : 'none';
        }

        async function createNewFamily() {
            const familyName = document.getElementById('familyName').value;

            try {
                const response = await fetch('/families', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({group_name: familyName})
                });

                if (!response.ok) throw new Error(await response.text());


                document.getElementById('familyName').value = '';
                toggleAddFamilyForm();
                await loadFamilies();
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Ошибка создания семьи: ' + error.message);
            }
        }

        function toggleAddUserForm() {
            const form = document.getElementById('addUserForm');
            isFormVisible = !isFormVisible;
            form.style.display = isFormVisible ? 'block' : 'none';
        }

        async function addNewUser() {
            const familyName = document.getElementById('familySelect').value;
            const newUser = {
                name: document.getElementById('userName').value,
                surname: document.getElementById('userSurname').value,
                email: document.getElementById('userEmail').value,
                password: document.getElementById('userPassword').value
            };

            try {
                const response = await fetch(`/families/${familyName}/users`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(newUser)
                });

                if (!response.ok) throw new Error(await response.text());


                toggleAddUserForm();
                await loadFamilyData(familyName);
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Ошибка при добавлении пользователя: ' + error.message);
            }
        }
