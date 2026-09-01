// ===== SORTABLE DRAG & DROP =====
const columns = ["todo", "inprogress", "done"];

columns.forEach(col => {
    Sortable.create(document.getElementById(col), {
        group: "kanban",
        animation: 150,
        ghostClass: "sortable-ghost",
        onEnd: function (evt) {
            const taskId = evt.item.dataset.id;
            const newStatus = evt.to.id;
            updateTaskStatus(taskId, newStatus);
        }
    });
});

function updateTaskStatus(taskId, status) {
    fetch(`/projects/task/update/${taskId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: status })
    });
}

// ===== MODAL =====
function openTaskModal() {
    document.getElementById("task-modal").classList.add("open");
}

function closeTaskModal() {
    document.getElementById("task-modal").classList.remove("open");
    document.getElementById("task-title").value = "";
    document.getElementById("task-desc").value = "";
    document.getElementById("task-employee").value = "";
    document.getElementById("task-due").value = "";
    document.getElementById("task-status").value = "todo";
}

// ===== ADD TASK =====
function submitTask() {
    const title = document.getElementById("task-title").value.trim();
    if (!title) {
        alert("Title is required");
        return;
    }

    const data = {
        title: title,
        description: document.getElementById("task-desc").value.trim(),
        employee_id: document.getElementById("task-employee").value || null,
        due_date: document.getElementById("task-due").value || null,
        status: document.getElementById("task-status").value,
        project_id: PROJECT_ID
    };

    fetch("/projects/task/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        if (res.success) {
            closeTaskModal();
            location.reload();
        }
    });
}

// ===== DELETE TASK =====
function deleteTask(taskId, btn) {
    if (!confirm("Delete this task?")) return;

    fetch(`/projects/task/delete/${taskId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    })
    .then(res => res.json())
    .then(res => {
        if (res.success) {
            btn.closest(".kanban-card").remove();
        }
    });
}

// ===== CLOSE MODAL ON OVERLAY CLICK =====
document.getElementById("task-modal").addEventListener("click", function(e) {
    if (e.target === this) closeTaskModal();
});