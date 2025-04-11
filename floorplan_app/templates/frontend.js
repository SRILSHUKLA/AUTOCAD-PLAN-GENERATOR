// Handle file selection
const fileInput = document.getElementById('file-input');
const fileName = document.getElementById('file-name');

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        fileName.textContent = e.target.files[0].name;
        fileName.style.display = 'block';
        
        // Add animation to the button
        gsap.to('.convert-btn', {
            scale: 1.05,
            duration: 0.3,
            repeat: 1,
            yoyo: true
        });
    }
});

// 3D background with Three.js
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
container.appendChild(renderer.domElement);

// Add grid lines to represent blueprints
const gridHelper = new THREE.GridHelper(100, 50, 0x5ee6d0, 0x36a18b);
scene.add(gridHelper);

// Add some floating particles
const particles = new THREE.Group();
scene.add(particles);

for (let i = 0; i < 100; i++) {
    const geometry = new THREE.BoxGeometry(0.2, 0.2, 0.2);
    const material = new THREE.MeshBasicMaterial({ 
        color: 0x5ee6d0, 
        transparent: true,
        opacity: Math.random() * 0.5 + 0.1
    });
    const particle = new THREE.Mesh(geometry, material);
    
    particle.position.x = Math.random() * 40 - 20;
    particle.position.y = Math.random() * 40 - 20;
    particle.position.z = Math.random() * 40 - 20;
    
    particle.userData = {
        vx: Math.random() * 0.02 - 0.01,
        vy: Math.random() * 0.02 - 0.01,
        vz: Math.random() * 0.02 - 0.01
    };
    
    particles.add(particle);
}

// Position camera
camera.position.z = 30;
camera.position.y = 15;
camera.lookAt(0, 0, 0);

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    
    // Rotate grid slowly
    gridHelper.rotation.y += 0.001;
    
    // Animate particles
    particles.children.forEach(particle => {
        particle.position.x += particle.userData.vx;
        particle.position.y += particle.userData.vy;
        particle.position.z += particle.userData.vz;
        
        // If particle goes too far, reset its position
        if (Math.abs(particle.position.x) > 30 || 
            Math.abs(particle.position.y) > 30 || 
            Math.abs(particle.position.z) > 30) {
            particle.position.x = Math.random() * 20 - 10;
            particle.position.y = Math.random() * 20 - 10;
            particle.position.z = Math.random() * 20 - 10;
        }
    });
    
    renderer.render(scene, camera);
}

// Handle window resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// Interactive card movement
const card = document.querySelector('.card');
window.addEventListener('mousemove', (e) => {
    if (window.innerWidth > 768) {
        const xAxis = (window.innerWidth / 2 - e.pageX) / 25;
        const yAxis = (window.innerHeight / 2 - e.pageY) / 25;
        card.style.transform = `rotateY(${xAxis}deg) rotateX(${yAxis}deg)`;
    }
});

// Start animation
animate();