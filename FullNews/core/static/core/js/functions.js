function confirmarBorrar(id) {
    Swal.fire({
        title: "¿Estas seguro?",
        text: "Esta accion no se revertirá",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Eliminar",
        cancelButtonText: "Cancelar"
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire({
            title: "Eliminado",
            text: "borrada",
            icon: "success"
          }).then(function() {
            window.location.href = "/adminEliminar/"+id;
          });
        }
      });
}

function denegarNew(id) {
  Swal.fire({
      title: "¿Estas seguro?",
      text: "Esta accion no se revertirá",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Eliminar",
      cancelButtonText: "Cancelar"
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire({
          title: "Eliminado",
          text: "borrada",
          icon: "success"
        }).then(function() {
          window.location.href = "/adminEliminar/"+id;
        });
      }
    });
}

function aprobarNew(id) {
  Swal.fire({
      title: "¿Estas seguro?",
      text: "Esta accion no se revertirá",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Eliminar",
      cancelButtonText: "Cancelar"
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire({
          title: "Eliminado",
          text: "borrada",
          icon: "success"
        }).then(function() {
          window.location.href = "/adminEliminar/"+id;
        });
      }
    });
}

