document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('webgl-bg');
    if (!canvas || typeof THREE === 'undefined') return;

    // 1. Setup Scene, Camera, Renderer
    const scene = new THREE.Scene();
    
    // Use an orthographic-like feel or perspective. Perspective is better for 3D depth.
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 400;

    const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // optimize performance

    // 2. Create Particles (Stars/Cosmic Dust)
    const particleCount = 2000;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    const colorPalette = [
        new THREE.Color('#ff0000'), // Pure Red (Oriental)
        new THREE.Color('#ff4500'), // Orange Red (Dragon Fire)
        new THREE.Color('#ffd700'), // Gold (Prosperity)
        new THREE.Color('#ff8c00')  // Dark Orange (Ember)
    ];

    for (let i = 0; i < particleCount; i++) {
        // Spherical distribution
        const r = 800 * Math.cbrt(Math.random());
        const theta = Math.random() * 2 * Math.PI;
        const phi = Math.acos(2 * Math.random() - 1);

        const x = r * Math.sin(phi) * Math.cos(theta);
        const y = r * Math.sin(phi) * Math.sin(theta);
        const z = r * Math.cos(phi);

        positions[i * 3] = x;
        positions[i * 3 + 1] = y;
        positions[i * 3 + 2] = z;

        // Random color from palette
        const color = colorPalette[Math.floor(Math.random() * colorPalette.length)];
        colors[i * 3] = color.r;
        colors[i * 3 + 1] = color.g;
        colors[i * 3 + 2] = color.b;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    // Create a circular texture for particles programmatically (no external image needed)
    const getTexture = () => {
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = 32;
        tempCanvas.height = 32;
        const ctx = tempCanvas.getContext('2d');
        const gradient = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
        gradient.addColorStop(0, 'rgba(255,255,255,1)');
        gradient.addColorStop(0.2, 'rgba(255,255,255,0.8)');
        gradient.addColorStop(0.5, 'rgba(255,255,255,0.2)');
        gradient.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, 32, 32);
        const texture = new THREE.Texture(tempCanvas);
        texture.needsUpdate = true;
        return texture;
    };

    const material = new THREE.PointsMaterial({
        size: 4,
        vertexColors: true,
        map: getTexture(),
        transparent: true,
        blending: THREE.AdditiveBlending,
        depthWrite: false
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    // 3. Interactivity (Parallax Mouse Move)
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    const windowHalfX = window.innerWidth / 2;
    const windowHalfY = window.innerHeight / 2;

    document.addEventListener('mousemove', (event) => {
        mouseX = (event.clientX - windowHalfX);
        mouseY = (event.clientY - windowHalfY);
    });

    // Handle touch
    document.addEventListener('touchmove', (event) => {
        if (event.touches.length > 0) {
            mouseX = (event.touches[0].clientX - windowHalfX);
            mouseY = (event.touches[0].clientY - windowHalfY);
        }
    });

    // 4. Animation Loop
    const clock = new THREE.Clock();

    function animate() {
        requestAnimationFrame(animate);

        const elapsedTime = clock.getElapsedTime();

        // Slow rotation of the entire particle system
        particles.rotation.y = elapsedTime * 0.05;
        particles.rotation.z = elapsedTime * 0.02;

        // Smooth parallax camera movement
        targetX = mouseX * 0.1;
        targetY = mouseY * 0.1;
        
        camera.position.x += (targetX - camera.position.x) * 0.02;
        camera.position.y += (-targetY - camera.position.y) * 0.02;
        camera.lookAt(scene.position);

        renderer.render(scene, camera);
    }

    animate();

    // 5. Resize Handler
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
});
