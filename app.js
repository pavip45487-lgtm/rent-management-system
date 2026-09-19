const state = {
  currentUser: null,
  editingHouseId: null,
};

const selectors = {
  authSection: document.getElementById('authSection'),
  homeSection: document.getElementById('homeSection'),
  loginForm: document.getElementById('loginForm'),
  registerForm: document.getElementById('registerForm'),
  showLoginButton: document.getElementById('showLoginButton'),
  showRegisterButton: document.getElementById('showRegisterButton'),
  loginButton: document.getElementById('loginButton'),
  registerButton: document.getElementById('registerButton'),
  logoutButton: document.getElementById('logoutButton'),
  userInfo: document.getElementById('userInfo'),
  welcomeText: document.getElementById('welcomeText'),
  loginUsername: document.getElementById('loginUsername'),
  loginPassword: document.getElementById('loginPassword'),
  registerUsername: document.getElementById('registerUsername'),
  registerPassword: document.getElementById('registerPassword'),
  registerFullName: document.getElementById('registerFullName'),
  registerPhone: document.getElementById('registerPhone'),
  loginMessage: document.getElementById('loginMessage'),
  registerMessage: document.getElementById('registerMessage'),
  addHouseSection: document.getElementById('addHouseSection'),
  listSection: document.getElementById('listSection'),
  detailSection: document.getElementById('detailSection'),
  houseList: document.getElementById('houseList'),
  houseDetail: document.getElementById('houseDetail'),
  listTitle: document.getElementById('listTitle'),
  houseFormTitle: document.getElementById('houseFormTitle'),
  houseMessage: document.getElementById('houseMessage'),
  saveHouseButton: document.getElementById('saveHouseButton'),
  cancelHouseButton: document.getElementById('cancelHouseButton'),
  houseTitle: document.getElementById('houseTitle'),
  houseType: document.getElementById('houseType'),
  houseCategory: document.getElementById('houseCategory'),
  houseStatus: document.getElementById('houseStatus'),
  housePrice: document.getElementById('housePrice'),
  houseContact: document.getElementById('houseContact'),
  houseAddress: document.getElementById('houseAddress'),
  houseDescription: document.getElementById('houseDescription'),
  houseImages: document.getElementById('houseImages'),
  houseExtra: document.getElementById('houseExtra'),
};

const storage = {
  users: 'rms_users',
  houses: 'rms_houses',
  session: 'rms_session',
};

function getUsers() {
  return JSON.parse(localStorage.getItem(storage.users) || '[]');
}

function saveUsers(users) {
  localStorage.setItem(storage.users, JSON.stringify(users));
}

function getHouses() {
  return JSON.parse(localStorage.getItem(storage.houses) || '[]');
}

function saveHouses(houses) {
  localStorage.setItem(storage.houses, JSON.stringify(houses));
}

function setSession(username) {
  localStorage.setItem(storage.session, username);
}

function clearSession() {
  localStorage.removeItem(storage.session);
}

function getSessionUser() {
  return localStorage.getItem(storage.session);
}

function init() {
  const existingUsers = getUsers();
  if (!existingUsers.length) {
    saveUsers([]);
  }

  const existingHouses = getHouses();
  if (!existingHouses.length) {
    saveHouses([]);
  }

  bindEvents();
  const sessionUser = getSessionUser();
  if (sessionUser) {
    state.currentUser = sessionUser;
    showHomePage();
    renderHouseList('all');
  }
}

function bindEvents() {
  selectors.showLoginButton.addEventListener('click', () => toggleAuthTab('login'));
  selectors.showRegisterButton.addEventListener('click', () => toggleAuthTab('register'));
  selectors.loginButton.addEventListener('click', handleLogin);
  selectors.registerButton.addEventListener('click', handleRegister);
  selectors.logoutButton.addEventListener('click', logout);
  selectors.saveHouseButton.addEventListener('click', handleSaveHouse);
  selectors.cancelHouseButton.addEventListener('click', resetHouseForm);

  document.querySelectorAll('[data-action]').forEach((button) => {
    button.addEventListener('click', (event) => {
      const action = event.currentTarget.dataset.action;
      handleHomeAction(action);
    });
  });
}

function toggleAuthTab(tab) {
  if (tab === 'login') {
    selectors.showLoginButton.classList.add('active');
    selectors.showRegisterButton.classList.remove('active');
    selectors.loginForm.classList.remove('hidden');
    selectors.registerForm.classList.add('hidden');
  } else {
    selectors.showRegisterButton.classList.add('active');
    selectors.showLoginButton.classList.remove('active');
    selectors.registerForm.classList.remove('hidden');
    selectors.loginForm.classList.add('hidden');
  }
}

function handleLogin() {
  const username = selectors.loginUsername.value.trim();
  const password = selectors.loginPassword.value;
  selectors.loginMessage.textContent = '';

  if (!username || !password) {
    selectors.loginMessage.textContent = 'Username and password are required.';
    return;
  }

  const users = getUsers();
  const user = users.find((item) => item.username === username && item.password === password);
  if (!user) {
    selectors.loginMessage.textContent = 'Invalid credentials. Check username and password.';
    return;
  }

  state.currentUser = user.username;
  setSession(user.username);
  selectors.loginUsername.value = '';
  selectors.loginPassword.value = '';
  showHomePage();
  renderHouseList('all');
}

function handleRegister() {
  const username = selectors.registerUsername.value.trim();
  const password = selectors.registerPassword.value;
  const fullName = selectors.registerFullName.value.trim();
  const phone = selectors.registerPhone.value.trim();
  selectors.registerMessage.textContent = '';

  if (!username || !password || !fullName || !phone) {
    selectors.registerMessage.textContent = 'All registration fields are required.';
    return;
  }

  const users = getUsers();
  const alreadyExists = users.some((item) => item.username === username);
  if (alreadyExists) {
    selectors.registerMessage.textContent = 'Username already exists. Choose another.';
    return;
  }

  users.push({
    username,
    password,
    fullName,
    phone,
  });
  saveUsers(users);

  selectors.registerMessage.style.color = 'var(--success)';
  selectors.registerMessage.textContent = 'Registration successful! You can now log in.';
  selectors.registerUsername.value = '';
  selectors.registerPassword.value = '';
  selectors.registerFullName.value = '';
  selectors.registerPhone.value = '';
}

function logout() {
  clearSession();
  state.currentUser = null;
  selectors.userInfo.classList.add('hidden');
  selectors.homeSection.classList.add('hidden');
  selectors.authSection.classList.remove('hidden');
  resetHouseForm();
}

function showHomePage() {
  selectors.authSection.classList.add('hidden');
  selectors.homeSection.classList.remove('hidden');
  selectors.userInfo.classList.remove('hidden');
  selectors.welcomeText.textContent = `Welcome, ${state.currentUser}`;
  hideAllSubsections();
}

function handleHomeAction(action) {
  hideAllSubsections();

  if (action === 'add') {
    selectors.addHouseSection.classList.remove('hidden');
    selectors.houseFormTitle.textContent = state.editingHouseId ? 'Edit House Details' : 'Add House Details';
    selectors.houseMessage.textContent = '';
    return;
  }

  selectors.listSection.classList.remove('hidden');
  selectors.detailSection.classList.add('hidden');

  switch (action) {
    case 'view-all':
      selectors.listTitle.textContent = 'All Listings';
      renderHouseList('all');
      break;
    case 'view-rent':
      selectors.listTitle.textContent = 'For Rent';
      renderHouseList('Rent');
      break;
    case 'view-lease':
      selectors.listTitle.textContent = 'For Lease';
      renderHouseList('Lease');
      break;
    case 'view-sale':
      selectors.listTitle.textContent = 'For Sale';
      renderHouseList('Sale');
      break;
    case 'view-mine':
      selectors.listTitle.textContent = 'My Listings';
      renderHouseList('mine');
      break;
  }
}

function hideAllSubsections() {
  selectors.addHouseSection.classList.add('hidden');
  selectors.listSection.classList.add('hidden');
  selectors.detailSection.classList.add('hidden');
  selectors.houseMessage.textContent = '';
  state.editingHouseId = null;
}

function handleSaveHouse() {
  const title = selectors.houseTitle.value.trim();
  const type = selectors.houseType.value;
  const category = selectors.houseCategory.value;
  const status = selectors.houseStatus.value;
  const price = selectors.housePrice.value.trim();
  const contact = selectors.houseContact.value.trim();
  const address = selectors.houseAddress.value.trim();
  const description = selectors.houseDescription.value.trim();
  const images = selectors.houseImages.value
    .split(',')
    .map((url) => url.trim())
    .filter(Boolean);
  const extra = selectors.houseExtra.value.trim();

  if (!title || !price || !contact || !address || !description) {
    selectors.houseMessage.textContent = 'Title, price, contact, address, and description are required.';
    return;
  }

  const houses = getHouses();
  if (state.editingHouseId) {
    const houseIndex = houses.findIndex((house) => house.id === state.editingHouseId);
    if (houseIndex === -1) {
      selectors.houseMessage.textContent = 'Could not find the house you are editing.';
      return;
    }

    houses[houseIndex] = {
      ...houses[houseIndex],
      title,
      type,
      category,
      status,
      price,
      contact,
      address,
      description,
      images,
      extra,
      updatedAt: new Date().toISOString(),
    };
    saveHouses(houses);
    selectors.houseMessage.style.color = 'var(--success)';
    selectors.houseMessage.textContent = 'Listing updated successfully.';
  } else {
    const house = {
      id: `house-${Date.now()}`,
      owner: state.currentUser,
      title,
      type,
      category,
      status,
      price,
      contact,
      address,
      description,
      images,
      extra,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    houses.push(house);
    saveHouses(houses);
    selectors.houseMessage.style.color = 'var(--success)';
    selectors.houseMessage.textContent = 'House listing added successfully.';
  }

  resetHouseForm();
  selectors.listSection.classList.remove('hidden');
  selectors.listTitle.textContent = 'All Listings';
  renderHouseList('all');
}

function resetHouseForm() {
  selectors.houseTitle.value = '';
  selectors.houseType.value = '1BHK';
  selectors.houseCategory.value = 'Rent';
  selectors.houseStatus.value = 'Available';
  selectors.housePrice.value = '';
  selectors.houseContact.value = '';
  selectors.houseAddress.value = '';
  selectors.houseDescription.value = '';
  selectors.houseImages.value = '';
  selectors.houseExtra.value = '';
  selectors.houseMessage.textContent = '';
  selectors.houseMessage.style.color = 'var(--danger)';
  state.editingHouseId = null;
  selectors.addHouseSection.classList.add('hidden');
}

function renderHouseList(filter) {
  const houses = getHouses();
  let filtered = houses;

  if (filter === 'Rent' || filter === 'Lease' || filter === 'Sale') {
    filtered = houses.filter((house) => house.category === filter);
  } else if (filter === 'mine') {
    filtered = houses.filter((house) => house.owner === state.currentUser);
  }

  if (!filtered.length) {
    selectors.houseList.innerHTML = '<p>No house listings found for this view.</p>';
    return;
  }

  selectors.houseList.innerHTML = filtered
    .map((house) => {
      const isOwner = house.owner === state.currentUser;
      const imageUrl = house.images.length ? house.images[0] : '';
      return `
        <div class="house-card">
          <h3>${house.title}</h3>
          <div class="house-meta">
            <span>${house.type}</span>
            <span>${house.category}</span>
            <span>${house.status}</span>
            <span>${house.price}</span>
          </div>
          <p>${house.address}</p>
          ${imageUrl ? `<img src="${imageUrl}" alt="House image" style="width:100%;border-radius:12px;max-height:220px;object-fit:cover;" />` : ''}
          <div class="form-actions">
            <button class="button-primary" onclick="showHouseDetails('${house.id}')">View Details</button>
            ${isOwner ? `<button class="button-secondary" onclick="editHouse('${house.id}')">Edit</button>` : ''}
          </div>
        </div>
      `;
    })
    .join('');
}

window.showHouseDetails = function (houseId) {
  const houses = getHouses();
  const house = houses.find((item) => item.id === houseId);
  if (!house) return;

  selectors.addHouseSection.classList.add('hidden');
  selectors.listSection.classList.add('hidden');
  selectors.detailSection.classList.remove('hidden');

  const imageMarkup = house.images.length
    ? `<div class="detail-images">${house.images.map((url) => `<img src="${url}" alt="House image" />`).join('')}</div>`
    : '<p>No images provided.</p>';

  const isOwner = house.owner === state.currentUser;
  const editButton = isOwner ? `<button class="button-secondary" onclick="editHouse('${house.id}')">Edit Listing</button>` : '';
  const deleteButton = isOwner ? `<button class="button-secondary" onclick="deleteHouse('${house.id}')">Delete Listing</button>` : '';
  const soldButton = isOwner && house.status !== 'Sold' ? `<button class="button-primary" onclick="updateHouseStatus('${house.id}', 'Sold')">Mark Sold</button>` : '';

  selectors.houseDetail.innerHTML = `
    <div class="house-detail">
      <h3>${house.title}</h3>
      ${imageMarkup}
      <div class="house-meta">
        <span>${house.type}</span>
        <span>${house.category}</span>
        <span>${house.status}</span>
        <span>${house.price}</span>
      </div>
      <p><strong>Address:</strong> ${house.address}</p>
      <p><strong>Contact:</strong> ${house.contact}</p>
      <p><strong>Description:</strong> ${house.description}</p>
      <p><strong>Additional details:</strong> ${house.extra || 'None'}</p>
      <p><strong>Owner:</strong> ${house.owner}</p>
      <div class="form-actions">
        ${editButton}
        ${deleteButton}
        ${soldButton}
        <button class="button-secondary" onclick="handleHomeAction('view-all')">Back to Listings</button>
      </div>
    </div>
  `;
};

window.editHouse = function (houseId) {
  const houses = getHouses();
  const house = houses.find((item) => item.id === houseId);
  if (!house || house.owner !== state.currentUser) return;

  state.editingHouseId = houseId;
  selectors.houseFormTitle.textContent = 'Edit House Details';
  selectors.houseTitle.value = house.title;
  selectors.houseType.value = house.type;
  selectors.houseCategory.value = house.category;
  selectors.houseStatus.value = house.status;
  selectors.housePrice.value = house.price;
  selectors.houseContact.value = house.contact;
  selectors.houseAddress.value = house.address;
  selectors.houseDescription.value = house.description;
  selectors.houseImages.value = house.images.join(', ');
  selectors.houseExtra.value = house.extra;

  selectors.listSection.classList.add('hidden');
  selectors.detailSection.classList.add('hidden');
  selectors.addHouseSection.classList.remove('hidden');
};

window.deleteHouse = function (houseId) {
  const houses = getHouses();
  const remaining = houses.filter((item) => item.id !== houseId || item.owner !== state.currentUser);
  saveHouses(remaining);
  showHomePage();
  renderHouseList('mine');
};

window.updateHouseStatus = function (houseId, status) {
  const houses = getHouses();
  const houseIndex = houses.findIndex((item) => item.id === houseId);
  if (houseIndex === -1) return;

  houses[houseIndex].status = status;
  houses[houseIndex].updatedAt = new Date().toISOString();
  saveHouses(houses);
  showHouseDetails(houseId);
};

init();
