# Bytestream Protocol Specification v1

## 1. Overview

Bytestream is a secure messaging protocol that uses a Web3 wallet for initial key derivation and Ed25519/X25519 for message signing and encryption.  
All cryptographic operations are performed client-side; the server never sees private keys.

## 2. Identity and Master Key

- The user signs a fixed message with their Ethereum wallet (e.g., MetaMask).
- The signature is used as input to HKDF (SHA-256) with salt `superchat_salt_v1` and info `master_key`.
- An optional PIN code may be appended to the fixed message. If set, the user must remember it to recover the same master key.
- Master key is 32 bytes and never leaves the device.

## 3. Device Keys

From the master key, derive two key pairs using HKDF:

- **X25519** key pair (for ECDH shared secret) – info `x25519`.
- **Ed25519** key pair (for message signing) – info `ed25519`.

## 4. Message Payload

Each message is identified by a unique `message_id` (12 random bytes) and a timestamp in milliseconds (Unix time).  
The content (text or file) is hashed together with `message_id` to produce a `content_hash`.

### 4.1 Fields

| Field | Type | Size (bytes) | Description |
|-------|------|-------------|-------------|
| message_id | bytes | 12 | Cryptographically random, used as salt and AES-GCM nonce |
| timestamp_ms | int | 8 (big-endian) | Unix time in milliseconds |
| content_hash | bytes | 32 | SHA-256(message_id + content) |

### 4.2 Signing Payload

The signing payload is the concatenation of the three fields:
payload = message_id || pack(timestamp_ms) || content_hash
Total length: 12 + 8 + 32 = 52 bytes.

## 5. Signing and Verification

- **Signing:** `Ed25519.sign(payload)` returns a 64-byte signature.
- **Verification:** `Ed25519.verify(signature, payload)` must succeed; any mismatch throws `InvalidSignature`.

## 6. Encryption (Optional)

Messages may be encrypted with AES-256-GCM.

- **Key:** derived via X25519 ECDH between sender and recipient.
- **Nonce:** the `message_id` (12 bytes) is reused as the AES-GCM nonce.
- **Encryption flag:** `is_encrypted` boolean in the transport JSON indicates whether the content field contains ciphertext or plaintext.

## 7. Transport JSON

The client sends a JSON object with the following fields:

```json
{
  "message_id": "<base64>",
  "timestamp": 1737381207123,
  "content_hash": "<base64>",
  "signature": "<base64>",
  "is_encrypted": true,
  "content": "<base64 or plaintext string>"
}
```

- message_id, content_hash, signature are base64-encoded.

- timestamp is a JSON number (milliseconds).

- If is_encrypted is false, content is a UTF-8 string. If true, content is base64 of the AES-GCM ciphertext.

- There is no separate nonce field; the nonce is the message_id itself.

## 8. Algorithms and Constants

HKDF: SHA-256, salt superchat_salt_v1, info master_key.

Key derivation info: x25519, ed25519.

X25519: ECDH.

Ed25519: signing and verification.

AES-256-GCM: encryption/decryption.

SHA-256: content hash.

Timestamp packing: 8-byte big-endian unsigned integer.

Fixed signing message: "Bytestream v1: Generate messaging keys for this device." (see app/constants.py).

PIN warning message: "WARNING: You have set a PIN code. You must remember it to recover your keys."

## 9. Security Considerations

Replay protection: unique message_id and timestamp ensure each signature payload is unique.

Content privacy: content_hash is salted with message_id to prevent rainbow table attacks.

Non-repudiation: signature covers the original content (via hash), not just ciphertext.

Forward secrecy: not provided in this version (static ECDH keys). Future versions may implement ephemeral keys.

Server trust: server stores only public keys and delivers encrypted blobs; it cannot read or forge messages.
