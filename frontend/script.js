let isFamilyFormVisible = false;
let isUserFormVisible = false;
let isPurchaseFormVisible = false;
let financeChart = null;

// Карта цветов для разных тегов
const tagColors = {
    'пополнение': '#2ecc71', // зеленый для пополнения
    'еда': '#f1c40f',       // желтый для еды
    'транспорт': '#e74c3c', // красный для транспорта
    'развлечения': '#9b59b6', // фиолетовый для развлечений
    'досуг': '#3498db',     // синий для досуга
    'другое': '#95a5a6',    // серый для других
};

// Функция для получения цвета по тегу
function getColorForTag(tag) {
    return tagColors[tag.toLowerCase()] || '#7f8c8d'; // Серый по умолчанию
}

document.addEventListener('DOMContentLoaded', async () => {
    await loadFamilies();
    
    // Инициализация форм
    document.getElementById('topUpForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const familyId = document.getElementById('familySelect').value;
        if (!familyId) {
            alert('Пожалуйста, выберите семью');
            return;
        }
        await addTopUp(familyId);
    });
    
    document.getElementById('deleteForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const familyId = document.getElementById('familySelect').value;
        if (!familyId) {
            alert('Пожалуйста, выберите семью');
            return;
        }
        await deleteTransaction(familyId);
    });
});

async function loadFamilies() {
    try {
        const response = await fetch('/families');
        if (!response.ok) {
            throw new Error('Failed to fetch families');
        }
        const families = await response.json();

        const select = document.getElementById('familySelect');
        select.innerHTML = '<option value="">Выберите семью...</option>';
        
        families.forEach(family => {
            const option = document.createElement('option');
            option.value = family.id;
            option.textContent = family.group_name;
            select.appendChild(option);
        });
        
        document.getElementById('totalFamilies').textContent = families.length;
    } catch (error) {
        console.error('Ошибка загрузки семей:', error);
        alert('Ошибка загрузки данных. Проверьте консоль.');
    }
}

async function loadFamilyData(familyId) {
    if (!familyId) {
        document.getElementById('familyInfo').style.display = 'none';
        return;
    }

    try {
        // Получаем данные о семье
        const response = await fetch(`/families/${familyId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch family data');
        }
        const familyData = await response.json();

        // Получаем список транзакций
        const transactionsResponse = await fetch(`/families/${familyId}/transactions`);
        const transactions = await transactionsResponse.json();
        
        // Получаем список пользователей семьи
        const usersResponse = await fetch(`/families/${familyId}/users`);
        if (!usersResponse.ok) {
            throw new Error('Failed to fetch users');
        }
        const users = await usersResponse.json();
        
        // Отображаем теги семьи
        if (familyData.tags && Array.isArray(familyData.tags)) {
            document.getElementById('familyTags').textContent = familyData.tags.join(', ');
            
            // Заполняем выпадающий список тегов для покупок
            const tagSelect = document.getElementById('purchaseTag');
            tagSelect.innerHTML = '<option value="">Выберите тег...</option>';
            
            familyData.tags.forEach(tag => {
                const option = document.createElement('option');
                option.value = tag;
                option.textContent = tag;
                tagSelect.appendChild(option);
            });
        } else {
            document.getElementById('familyTags').textContent = 'Нет тегов';
        }
        
        // Обновляем выпадающие списки пользователей
        const userSelects = [
            document.getElementById('purchaseUser'),
            document.getElementById('topUpUser')
        ];
        
        userSelects.forEach(userSelect => {
            if (userSelect) {
                userSelect.innerHTML = '<option value="">Выберите пользователя...</option>';
                
                if (Array.isArray(users) && users.length > 0) {
                    const userOptions = users.map(user => {
                        if (!user) return '';
                        return `<option value="${user.id}">${user.name}</option>`;
                    }).join('');
                    userSelect.innerHTML += userOptions;
                }
            }
        });

        // Обновляем метаданные семьи
        document.getElementById('createdAt').textContent = familyData.created_at ? 
            new Date(familyData.created_at).toLocaleDateString('ru-RU') : 'Не указано';
        document.getElementById('totalBalance').textContent = `${calculateBalance(transactions)} ₽`;
        document.getElementById('lastActivity').textContent = new Date().toLocaleDateString('ru-RU');

        // Показываем количество участников
        document.getElementById('membersCount').textContent = 
            Array.isArray(users) ? users.length : 0;
        
        // Расчет расходов
        const expenditure = Array.isArray(transactions) ? 
            transactions
                .filter(tx => tx && tx.amount < 0)
                .reduce((sum, tx) => sum + Math.abs(tx.amount || 0), 0) : 0;
            
        document.getElementById('totalExpenditure').textContent = `${expenditure} ₽`;

        // Обновляем список пользователей в интерфейсе
        const usersList = document.getElementById('usersList');
        if (Array.isArray(users) && users.length > 0) {
            usersList.innerHTML = users.map(user => {
                if (!user) return '';
                const name = user.name || 'Без имени';
                // Получаем инициалы для аватара
                const nameInitial = name.length > 0 ? name[0] : '?';
                
                return `
                <div class="d-flex align-items-center gap-3 p-2 bg-light rounded">
                    <div class="user-avatar">
                        ${nameInitial}
                    </div>
                    <div>
                        <div class="fw-bold">${name}</div>
                        <small class="text-muted">${user.email || 'Нет email'}</small>
                    </div>
                </div>
                `;
            }).join('');
        } else {
            usersList.innerHTML = '<div class="text-muted">Нет пользователей</div>';
        }

        // Отображаем транзакции
        const purchasesList = document.getElementById('purchasesList');
        const purchases = Array.isArray(transactions) ? 
            transactions.filter(tx => tx && tx.amount < 0) : [];
            
        if (purchases.length > 0) {
            purchasesList.innerHTML = purchases.map(purchase => {
                if (!purchase) return '';
                // Находим имя пользователя по ID
                const userId = purchase.user_id;
                const user = users.find(u => u.id === userId);
                const userName = user ? user.name : 'Неизвестный';
                
                // Получаем теги
                const tags = purchase.tags && Array.isArray(purchase.tags) && purchase.tags.length > 0 
                    ? purchase.tags.join(', ') 
                    : 'Без категории';
                
                // Определяем цвет для тега (берем первый тег для цвета)
                const tagForColor = purchase.tags && purchase.tags.length > 0 ? purchase.tags[0] : 'другое';
                const tagColor = getColorForTag(tagForColor);
                
                return `
                <div class="purchase-item">
                    <div>
                        <div class="fw-bold">${tags}</div>
                        <small class="text-muted">${userName}, ${new Date(purchase.created_at).toLocaleDateString('ru-RU')}</small>
                    </div>
                    <div class="text-danger fw-bold" style="color: ${tagColor} !important;">
                        ${Math.abs(purchase.amount).toLocaleString()} ₽
                    </div>
                </div>
                `;
            }).join('');
        } else {
            purchasesList.innerHTML = '<div class="text-muted">Нет покупок</div>';
        }

        // График финансов с разбивкой по тегам
        if (financeChart) {
            financeChart.destroy();
        }
        
        // Группируем транзакции по тегам
        const tagTotals = {};
        if (Array.isArray(transactions)) {
            transactions.forEach(tx => {
                if (!tx || !tx.tags || !Array.isArray(tx.tags) || tx.tags.length === 0) {
                    const tag = tx && tx.amount > 0 ? 'пополнение' : 'другое';
                    tagTotals[tag] = (tagTotals[tag] || 0) + Math.abs(tx.amount || 0);
                } else {
                    const tag = tx.amount > 0 ? 'пополнение' : tx.tags[0]; // Используем первый тег
                    tagTotals[tag] = (tagTotals[tag] || 0) + Math.abs(tx.amount || 0);
                }
            });
        }
        
        const chartLabels = Object.keys(tagTotals);
        const chartData = Object.values(tagTotals);
        const chartColors = chartLabels.map(tag => getColorForTag(tag));
        
        const ctx = document.getElementById('financeChart').getContext('2d');
        financeChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: chartLabels,
                datasets: [{
                    data: chartData,
                    backgroundColor: chartColors
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });

        document.getElementById('familyInfo').style.display = 'flex';
    } catch (error) {
        console.error('Ошибка загрузки данных семьи:', error);
        alert('Ошибка загрузки данных семьи');
    }
}

// Вспомогательная функция для расчета общего баланса
function calculateBalance(transactions) {
    if (!Array.isArray(transactions)) return 0;
    return transactions.reduce((sum, tx) => sum + (tx.amount || 0), 0);
}

function toggleAddFamilyForm() {
    const form = document.getElementById('addFamilyForm');
    isFamilyFormVisible = !isFamilyFormVisible;
    form.style.display = isFamilyFormVisible ? 'block' : 'none';
}

function toggleAddUserForm() {
    const form = document.getElementById('addUserForm');
    isUserFormVisible = !isUserFormVisible;
    form.style.display = isUserFormVisible ? 'block' : 'none';
}

function toggleAddPurchaseForm() {
    const form = document.getElementById('addPurchaseForm');
    isPurchaseFormVisible = !isPurchaseFormVisible;
    form.style.display = isPurchaseFormVisible ? 'block' : 'none';
}

async function createNewFamily() {
    const familyName = document.getElementById('familyName').value;

    try {
        const response = await fetch('/families', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ group_name: familyName })
        });

        if (!response.ok) {
            throw new Error('Failed to create family');
        }

        document.getElementById('familyName').value = '';
        toggleAddFamilyForm();
        await loadFamilies();
    } catch (error) {
        console.error('Ошибка создания семьи:', error);
        alert('Ошибка при создании новой семьи');
    }
}

async function addNewUser() {
    const familyId = document.getElementById('familySelect').value;
    if (!familyId) {
        alert('Пожалуйста, выберите семью');
        return;
    }
    
    const newUser = {
        name: document.getElementById('userName').value,
        email: document.getElementById('userEmail').value,
        password: document.getElementById('userPassword').value
    };

    try {
        const response = await fetch(`/families/${familyId}/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newUser)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Failed to add user: ${errorData.detail || 'Unknown error'}`);
        }

        document.getElementById('userName').value = '';
        document.getElementById('userSurname').value = '';
        document.getElementById('userEmail').value = '';
        document.getElementById('userPassword').value = '';
        
        toggleAddUserForm();
        await loadFamilyData(familyId);
    } catch (error) {
        console.error('Ошибка добавления пользователя:', error);
        alert(`Ошибка при добавлении пользователя: ${error.message}`);
    }
}

async function addNewPurchase() {
    const familyId = document.getElementById('familySelect').value;
    if (!familyId) {
        alert('Пожалуйста, выберите семью');
        return;
    }
    
    const userId = document.getElementById('purchaseUser').value;
    if (!userId) {
        alert('Пожалуйста, выберите пользователя');
        return;
    }
    
    const tag = document.getElementById('purchaseTag').value;
    const description = document.getElementById('purchaseDesc').value;
    
    // Формируем массив тегов, включая выбранный тег и описание как отдельный тег
    const tags = [];
    if (tag) tags.push(tag);
    if (description) tags.push(description);
    
    // Если тегов нет, добавим "другое"
    if (tags.length === 0) {
        tags.push("другое");
    }
    
    const newPurchase = {
        user_id: userId,
        price: parseFloat(document.getElementById('purchasePrice').value),
        tags: tags,
        date: new Date().toLocaleDateString('ru-RU')  // Текущая дата в формате ДД.ММ.ГГГГ
    };

    try {
        const response = await fetch(`/families/${familyId}/purchases`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newPurchase)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Failed to add purchase: ${errorData.detail || 'Unknown error'}`);
        }

        document.getElementById('purchasePrice').value = '';
        document.getElementById('purchaseDesc').value = '';
        document.getElementById('purchaseTag').value = '';
        
        toggleAddPurchaseForm();
        await loadFamilyData(familyId);
    } catch (error) {
        console.error('Ошибка добавления покупки:', error);
        alert(`Ошибка при добавлении покупки: ${error.message}`);
    }
}

async function addTopUp(familyId) {
    const userId = document.getElementById('topUpUser').value;
    if (!userId) {
        alert('Пожалуйста, выберите пользователя для пополнения');
        return;
    }
    
    const amount = parseFloat(document.getElementById('topUpAmount').value);
    
    const topUpData = {
        user_id: userId,
        amount: amount,
        tags: ["пополнение"],
        date: new Date().toLocaleDateString('ru-RU')  // Текущая дата в формате ДД.ММ.ГГГГ
    };
    
    try {
        const response = await fetch(`/families/${familyId}/topups`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(topUpData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Failed to add top-up: ${errorData.detail || 'Unknown error'}`);
        }

        document.getElementById('topUpAmount').value = '';
        await loadFamilyData(familyId);
    } catch (error) {
        console.error('Ошибка пополнения:', error);
        alert(`Ошибка при пополнении баланса: ${error.message}`);
    }
}

async function deleteTransaction(familyId) {
    const transactionId = document.getElementById('transaction-id').value;
    
    try {
        const response = await fetch(`/families/${familyId}/transactions/${transactionId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Failed to delete transaction');
        }

        document.getElementById('transaction-id').value = '';
        await loadFamilyData(familyId);
    } catch (error) {
        console.error('Ошибка удаления транзакции:', error);
        alert('Ошибка при удалении транзакции');
    }
}
