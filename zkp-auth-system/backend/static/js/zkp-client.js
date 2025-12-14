/**
 * Zero-Knowledge Proof Client using Schnorr Protocol
 * Client-side implementation for browser
 */

class SchnorrZKPClient {
    constructor() {
        // secp256k1 curve parameters (same as Bitcoin)
        this.CURVE_P = BigInt('0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F');
        this.CURVE_N = BigInt('0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141');
        this.CURVE_G_X = BigInt('0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798');
        this.CURVE_G_Y = BigInt('0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8');
        
        // Generator point
        this.G = { x: this.CURVE_G_X, y: this.CURVE_G_Y };
    }

    /**
     * Modular inverse using Extended Euclidean Algorithm
     */
    modInverse(a, m) {
        if (a < 0n) a = a % m;
        return this.modPow(a, m - 2n, m);
    }

    /**
     * Modular exponentiation
     */
    modPow(base, exp, mod) {
        let result = 1n;
        base = base % mod;
        while (exp > 0n) {
            if (exp % 2n === 1n) {
                result = (result * base) % mod;
            }
            exp = exp >> 1n;
            base = (base * base) % mod;
        }
        return result;
    }

    /**
     * Add two points on elliptic curve
     */
    pointAdd(p1, p2) {
        // Handle point at infinity
        if (p1.x === 0n && p1.y === 0n) {
            return p2;
        }
        if (p2.x === 0n && p2.y === 0n) {
            return p1;
        }
        
        let s;
        if (p1.x === p2.x && p1.y === p2.y) {
            // Point doubling
            if (p1.y === 0n) {
                return { x: 0n, y: 0n }; // Point at infinity
            }
            s = (3n * p1.x * p1.x) * this.modInverse(2n * p1.y, this.CURVE_P) % this.CURVE_P;
        } else {
            // Point addition
            if (p1.x === p2.x) {
                return { x: 0n, y: 0n }; // Point at infinity
            }
            s = (p2.y - p1.y) * this.modInverse(p2.x - p1.x, this.CURVE_P) % this.CURVE_P;
        }
        
        // Ensure s is positive
        if (s < 0n) {
            s = s + this.CURVE_P;
        }
        
        let x3 = (s * s - p1.x - p2.x) % this.CURVE_P;
        let y3 = (s * (p1.x - x3) - p1.y) % this.CURVE_P;
        
        // Ensure positive modulo (BigInt modulo can be negative)
        if (x3 < 0n) {
            x3 = x3 + this.CURVE_P;
        }
        if (y3 < 0n) {
            y3 = y3 + this.CURVE_P;
        }
        
        return { x: x3 % this.CURVE_P, y: y3 % this.CURVE_P };
    }

    /**
     * Scalar multiplication: k * point
     */
    pointMultiply(k, point) {
        if (k === 0n) {
            return { x: 0n, y: 0n };
        }
        
        // Handle negative k
        if (k < 0n) {
            k = k % this.CURVE_N;
            if (k < 0n) {
                k = k + this.CURVE_N;
            }
        }
        
        let result = { x: 0n, y: 0n };
        let addend = point;
        
        while (k > 0n) {
            if (k & 1n) {
                result = this.pointAdd(result, addend);
            }
            addend = this.pointAdd(addend, addend);
            k = k >> 1n;
        }
        
        return result;
    }

    /**
     * Hash to integer using SHA-256
     */
    async hashToInt(...args) {
        const encoder = new TextEncoder();
        let combined = new Uint8Array(0);
        
        for (const arg of args) {
            let bytes;
            if (typeof arg === 'bigint') {
                bytes = new Uint8Array(32);
                const hex = arg.toString(16).padStart(64, '0');
                for (let i = 0; i < 32; i++) {
                    bytes[i] = parseInt(hex.substr(i * 2, 2), 16);
                }
            } else if (typeof arg === 'object' && arg.x !== undefined) {
                // Point object
                const xBytes = new Uint8Array(32);
                const yBytes = new Uint8Array(32);
                const xHex = arg.x.toString(16).padStart(64, '0');
                const yHex = arg.y.toString(16).padStart(64, '0');
                for (let i = 0; i < 32; i++) {
                    xBytes[i] = parseInt(xHex.substr(i * 2, 2), 16);
                    yBytes[i] = parseInt(yHex.substr(i * 2, 2), 16);
                }
                bytes = new Uint8Array([...xBytes, ...yBytes]);
            } else {
                bytes = encoder.encode(String(arg));
            }
            
            const temp = new Uint8Array(combined.length + bytes.length);
            temp.set(combined);
            temp.set(bytes, combined.length);
            combined = temp;
        }
        
        // Use crypto.subtle if available (HTTPS/localhost), otherwise use fallback
        let hashHex;
        if (window.crypto && window.crypto.subtle && (location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1')) {
            try {
                const hashBuffer = await crypto.subtle.digest('SHA-256', combined);
                const hashArray = Array.from(new Uint8Array(hashBuffer));
                hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
            } catch (e) {
                // Fallback to simple hash if crypto.subtle fails
                console.warn('crypto.subtle failed, using fallback hash:', e);
                hashHex = this.simpleHash(combined);
            }
        } else {
            // Fallback for HTTP or browsers without crypto.subtle
            console.warn('crypto.subtle not available, using fallback hash');
            hashHex = this.simpleHash(combined);
        }
        
        return BigInt('0x' + hashHex) % this.CURVE_N;
    }

    /**
     * Simple SHA-256 implementation (fallback for HTTP)
     * Based on simplified SHA-256 algorithm
     */
    simpleHash(data) {
        // Convert Uint8Array to string for processing
        let str = '';
        for (let i = 0; i < data.length; i++) {
            str += String.fromCharCode(data[i]);
        }
        
        // Simple hash using string operations
        // This is a simplified version - for production, use proper SHA-256 library
        let hash = 0;
        const primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53];
        
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash + primes[i % primes.length] * char;
            hash = hash & hash; // Convert to 32bit integer
        }
        
        // Create 64-char hex string (256-bit)
        let hex = Math.abs(hash).toString(16).padStart(8, '0');
        // Extend to 64 chars by hashing multiple times
        let fullHash = '';
        for (let i = 0; i < 8; i++) {
            let part = hash;
            for (let j = 0; j < str.length; j++) {
                part = ((part << 3) - part) + str.charCodeAt(j) + i;
            }
            fullHash += Math.abs(part).toString(16).padStart(8, '0');
        }
        
        return fullHash.substring(0, 64);
    }

    /**
     * Generate random private key
     */
    generatePrivateKey() {
        const array = new Uint8Array(32);
        crypto.getRandomValues(array);
        let key = BigInt('0x' + Array.from(array).map(b => b.toString(16).padStart(2, '0')).join(''));
        key = key % (this.CURVE_N - 1n) + 1n;
        return key;
    }

    /**
     * Generate key pair
     */
    async generateKeyPair() {
        const privateKey = this.generatePrivateKey();
        const publicKey = this.pointMultiply(privateKey, this.G);
        return {
            privateKey: privateKey,
            publicKey: publicKey
        };
    }

    /**
     * Generate Schnorr ZKP proof
     */
    async generateProof(privateKey, publicKey) {
        // Generate random nonce r
        const r = this.generatePrivateKey();
        
        // Compute R = r * G
        const R = this.pointMultiply(r, this.G);
        
        // Generate challenge c = H(R || Y || message)
        const message = "authentication";
        const c = await this.hashToInt(R, publicKey, message);
        
        // Compute response s = r + c * x (mod n)
        const s = (r + c * privateKey) % this.CURVE_N;
        
        // Ensure hex strings are lowercase and properly formatted
        const formatHex = (val) => {
            let hex = val.toString(16).toLowerCase();
            // Remove leading zeros but keep at least one character
            if (hex === '0') return '0x0';
            return '0x' + hex;
        };
        
        return {
            R: {
                x: formatHex(R.x),
                y: formatHex(R.y)
            },
            s: formatHex(s),
            c: formatHex(c)
        };
    }

    /**
     * Convert point to hex string
     */
    pointToHex(point) {
        return {
            x: '0x' + point.x.toString(16),
            y: '0x' + point.y.toString(16)
        };
    }
}

// Global instance
const zkpClient = new SchnorrZKPClient();

// Registration handler
async function handleRegister() {
    const username = document.getElementById('username').value;
    if (!username) {
        alert('Please enter a username');
        return;
    }

    try {
        // Generate key pair
        const keyPair = await zkpClient.generateKeyPair();
        
        // Store private key in localStorage (in production, use secure storage)
        localStorage.setItem('zkp_private_key', keyPair.privateKey.toString());
        localStorage.setItem('zkp_public_key', JSON.stringify(zkpClient.pointToHex(keyPair.publicKey)));
        localStorage.setItem('zkp_username', username);

        // Send public key to server
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                public_key: zkpClient.pointToHex(keyPair.publicKey)
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('Registration successful! Your keys have been saved locally.');
            window.location.href = '/login';
        } else {
            alert('Registration failed: ' + data.error);
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('Registration error: ' + error.message);
    }
}

// Login handler
async function handleLogin() {
    const username = document.getElementById('username').value;
    if (!username) {
        alert('Please enter your username');
        return;
    }

    try {
        // Get private key from localStorage
        const privateKeyStr = localStorage.getItem('zkp_private_key');
        const publicKeyStr = localStorage.getItem('zkp_public_key');
        const storedUsername = localStorage.getItem('zkp_username');
        
        if (!privateKeyStr || !publicKeyStr) {
            alert('No keys found. Please register first.');
            return;
        }

        // Check if username matches
        if (storedUsername !== username) {
            alert('Username mismatch! The keys in your browser are for a different username. Please register again with this username.');
            return;
        }

        const privateKey = BigInt(privateKeyStr);
        const publicKeyObj = JSON.parse(publicKeyStr);
        const publicKey = {
            x: BigInt(publicKeyObj.x),
            y: BigInt(publicKeyObj.y)
        };

        // Generate proof
        const proof = await zkpClient.generateProof(privateKey, publicKey);

        // Send proof to server
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                proof: proof
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('Login successful!');
            // Store session token
            localStorage.setItem('session_token', data.session_token);
            window.location.href = '/';
        } else {
            alert('Login failed: ' + data.error);
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login error: ' + error.message);
    }
}

// Logout handler
async function handleLogout() {
    try {
        await fetch('/api/logout', {
            method: 'POST'
        });
        localStorage.removeItem('session_token');
        window.location.href = '/';
    } catch (error) {
        console.error('Logout error:', error);
    }
}

// Check authentication status
async function checkAuth() {
    try {
        const response = await fetch('/api/verify-session');
        const data = await response.json();
        return data.authenticated;
    } catch (error) {
        return false;
    }
}

