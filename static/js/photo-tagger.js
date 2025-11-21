// Photo Tagging JavaScript - Point Selection & Modal Implementation

let isTagging = false;
let currentPhotoId;
let tempMarker = null;
let currentCoords = null;

function initPhotoTagger(photoId) {
  currentPhotoId = photoId;
  const startButton = document.getElementById('startTagging');
  const photoImage = document.getElementById('photoImage');

  if (!startButton || !photoImage) {
    console.error('Required elements not found');
    return;
  }

  startButton.addEventListener('click', function () {
    isTagging = !isTagging;
    updateUIState();
  });

  photoImage.addEventListener('click', function (e) {
    if (!isTagging) return;

    const rect = photoImage.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Store coords as center point
    currentCoords = { x, y };

    // Show temp marker
    showTempMarker(x, y);

    // Open modal
    document.getElementById('taggingModal').style.display = 'block';

    // Focus search input and reset
    const searchInput = document.getElementById('userSearchInput');
    searchInput.value = '';
    searchInput.focus();
    filterUsers(); // Reset filter
  });

  // The saveBtn.addEventListener is removed as selection from the list now triggers saving
  // saveBtn.addEventListener('click', function () {
  //   const userSelect = document.getElementById('modalTagUser');
  //   const userId = userSelect.value;

  //   if (!userId) {
  //     alert('Lütfen bir kişi seçin');
  //     return;
  //   }

  //   // Create coords string (x1,y1,x2,y2) - creating a small box around the point for compatibility
  //   // We will use the center point for rendering
  //   const size = 20;
  //   const coords = `${Math.round(currentCoords.x - size / 2)},${Math.round(currentCoords.y - size / 2)},${Math.round(currentCoords.x + size / 2)},${Math.round(currentCoords.y + size / 2)}`;

  //   savePhotoTag(userId, 'rect', coords);
  // });
}

function updateUIState() {
  const startButton = document.getElementById('startTagging');
  const photoImage = document.getElementById('photoImage');

  if (isTagging) {
    startButton.textContent = 'İptal';
    startButton.classList.remove('btn-primary');
    startButton.classList.add('btn-danger');
    photoImage.style.cursor = 'crosshair';
  } else {
    startButton.textContent = 'Etiketlemeye Başla';
    startButton.classList.remove('btn-danger');
    startButton.classList.add('btn-primary');
    photoImage.style.cursor = 'default';
    removeTempMarker();
  }
}

function showTempMarker(x, y) {
  removeTempMarker();
  tempMarker = document.createElement('div');
  tempMarker.className = 'saved-tag';
  tempMarker.style.left = x + 'px';
  tempMarker.style.top = y + 'px';
  tempMarker.style.opacity = '0.5';
  tempMarker.style.pointerEvents = 'none';
  document.getElementById('photoTagger').appendChild(tempMarker);
}

function removeTempMarker() {
  if (tempMarker) {
    tempMarker.remove();
    tempMarker = null;
  }
}

function closeTaggingModal() {
  document.getElementById('taggingModal').style.display = 'none';
  removeTempMarker();
}

function filterUsers() {
  const input = document.getElementById('userSearchInput');
  const filter = input.value.toLowerCase();
  const ul = document.getElementById('userListSelect');
  const li = ul.getElementsByTagName('li');

  for (let i = 0; i < li.length; i++) {
    const span = li[i].getElementsByTagName('span')[0];
    const txtValue = span.textContent || span.innerText;
    if (txtValue.toLowerCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}

function selectUser(userId, userName) {
  // Create coords string (x1,y1,x2,y2) - creating a small box around the point for compatibility
  // We will use the center point for rendering
  const size = 20;
  const coords = `${Math.round(currentCoords.x - size / 2)},${Math.round(currentCoords.y - size / 2)},${Math.round(currentCoords.x + size / 2)},${Math.round(currentCoords.y + size / 2)}`;

  savePhotoTag(userId, 'rect', coords, userName);
}

async function savePhotoTag(userId, shape, coords, userName) {
  try {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    const response = await fetch(`/photos/${currentPhotoId}/tag`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({
        user_id: parseInt(userId),
        shape: shape,
        coords: coords
      })
    });

    const data = await response.json();

    if (data.success) {
      // Close modal
      closeTaggingModal();

      // Reset UI state (stop tagging mode)
      isTagging = false;
      updateUIState();

      // Create new tag element visually
      const tag = document.createElement('div');
      tag.className = 'saved-tag';
      tag.dataset.coords = coords;
      tag.dataset.user = userName;
      tag.dataset.id = data.tag_id;
      tag.onclick = function () { window.location.href = '/profile/' + userId; };

      // Add delete button
      const deleteBtn = document.createElement('div');
      deleteBtn.className = 'delete-tag-btn';
      deleteBtn.innerHTML = '&times;';
      deleteBtn.onclick = function (e) {
        e.stopPropagation();
        deleteTag(data.tag_id);
      };
      tag.appendChild(deleteBtn);

      document.getElementById('photoTagger').appendChild(tag);
      renderSavedTags();

      // Add to list
      const list = document.getElementById('taggedUsersList');
      const noTagsMsg = list.querySelector('.no-tags-msg');
      if (noTagsMsg) noTagsMsg.remove();

      const li = document.createElement('li');
      li.id = `tag-list-item-${data.tag_id}`;
      li.style.cssText = 'padding: 0.5rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); display: flex; justify-content: space-between; align-items: center;';
      li.innerHTML = `
        <a href="/profile/${userId}">${userName}</a>
        <button class="btn btn-sm btn-danger" onclick="deleteTag('${data.tag_id}')" style="padding: 2px 8px; font-size: 12px; border-radius: 4px;">Sil</button>
      `;
      list.appendChild(li);

      // Reset select (no longer needed as user selection is handled by filter/list)
      // userSelect.value = "";

    } else {
      alert('Etiket eklenirken hata oluştu.');
    }
  } catch (error) {
    console.error('Error saving tag:', error);
    alert('Etiket eklenirken hata oluştu.');
  }
}

async function deleteTag(tagId) {
  if (!confirm('Bu etiketi silmek istediğinize emin misiniz?')) {
    return;
  }

  try {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const response = await fetch(`/photos/${currentPhotoId}/tag/${tagId}`, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': csrfToken
      }
    });

    const data = await response.json();
    if (data.success) {
      // Remove from visual tags
      const tagElement = document.querySelector(`.saved-tag[data-id="${tagId}"]`);
      if (tagElement) tagElement.remove();

      // Remove from list
      const listItem = document.getElementById(`tag-list-item-${tagId}`);
      if (listItem) listItem.remove();

      // Check if list is empty
      const list = document.getElementById('taggedUsersList');
      if (list && list.children.length === 0) {
        list.innerHTML = '<li class="text-muted no-tags-msg">Henüz etiket yok</li>';
      }
    } else {
      alert('Etiket silinirken hata oluştu: ' + (data.message || 'Bilinmeyen hata'));
    }
  } catch (error) {
    console.error('Error deleting tag:', error);
    alert('Etiket silinirken hata oluştu.');
  }
}

function renderSavedTags() {
  const tags = document.querySelectorAll('.saved-tag');
  tags.forEach(tag => {
    // Skip temp marker
    if (tag === tempMarker) return;

    const coords = tag.dataset.coords.split(',');
    if (coords.length === 4) {
      const x1 = parseInt(coords[0]);
      const y1 = parseInt(coords[1]);
      const x2 = parseInt(coords[2]);
      const y2 = parseInt(coords[3]);

      // Calculate center
      const centerX = (x1 + x2) / 2;
      const centerY = (y1 + y2) / 2;

      tag.style.left = centerX + 'px';
      tag.style.top = centerY + 'px';
      // Width/Height are fixed in CSS for markers
    }
  });
}
