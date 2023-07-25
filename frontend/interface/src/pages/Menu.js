import React, { useState } from 'react';

const Menu = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [console1, setConsole1] = useState('');
  const [console2, setConsole2] = useState('');

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    readSelectedFile(file);
  };

  const readSelectedFile = (file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const fileContent = e.target.result;
      setConsole1(fileContent);
    };
    reader.readAsText(file);
  };

  const handleConsole1Change = (event) => {
    setConsole1(event.target.value);
  };

  
  const handleExecute = () => {
    const replacedConsole1 = console1.replace(/"/g, "'");
    // 
    // http://0.0.0.0:8000/command/console-command
    fetch('http://18.221.14.38:8000/command/console-command', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        command: replacedConsole1
      })
    })
      .then(response => response.json())
      .then(data => {
        // Actualizar la consola 2 con los resultados obtenidos
        setConsole2(data.message);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  
    console.log(JSON.stringify({
      command: replacedConsole1
    }));
  };
  
  


  const handleLogout = () => {
    window.location.href="./";
  };

  return (
    <div className="container py-4">
      <div className="container">
        <div className="row">
          <div className="col-12">
            <div className="button-container float-end">
              <button type="button" className="btn btn-danger" onClick={handleLogout}>Logout</button>
            </div>
          </div>
        </div>

        <div className="row">
          <div className="col-4">
            <div className="">
              <h5>Subir Archivos</h5>
              <form className="form">
                <input type="file" className="carga mt-3" id="file" name="file" onChange={handleFileChange} />
              </form>
            </div>
          </div>

          <div className="col-8">
            <div>
              <textarea className="form-control mt-4 taller-textarea" value={console1} onChange={handleConsole1Change}></textarea>
            </div>

            <div>
              <textarea className="form-control mt-4 taller-textarea" value={console2} readOnly></textarea>
            </div>

            <div>
              <button type="button" className="btn btn-primary mt-4" onClick={handleExecute}>Ejecutar</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Menu;



