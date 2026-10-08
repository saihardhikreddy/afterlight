/* SENTINEL ring station viewer: the SentinelSpread ship, space and post stack, with a
   drag turntable and one button per effect channel instead of the scroll story. */

import * as THREE from "three";
import { createPost } from "./js/world/post.js";
import { buildSpace } from "./js/world/space.js";
import { buildShip } from "./js/world/ship.js";

const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
const coarse = matchMedia("(pointer: coarse)").matches;
const canvas = document.getElementById("world");
const boot = document.getElementById("boot");
const finishBoot = () => boot.classList.add("is-done");
setTimeout(finishBoot, 8000); // never hold the page hostage

function notice(text) {
  const p = document.createElement("p");
  p.className = "notice"; p.setAttribute("role", "status"); p.textContent = text;
  document.body.append(p);
}

let renderer;
try {
  renderer = new THREE.WebGLRenderer({ canvas, antialias: false, alpha: false, powerPreference: "high-performance" });
} catch (e) {
  notice("WebGL isn't available in this browser, so the station can't render."); finishBoot();
  throw e;
}
renderer.setClearColor(0x03040a, 1);
renderer.toneMapping = THREE.NoToneMapping;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(40, 1, 0.05, 1200);
scene.add(camera);
const uniforms = { uTime: { value: 0 }, uScale: { value: 1000 }, uDim: { value: 1 } };
const space = buildSpace(scene, camera, uniforms);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
Object.assign(space.key.shadow.camera, { left: -17, right: 17, top: 17, bottom: -17, near: 20, far: 120 });
space.key.shadow.mapSize.set(coarse ? 1024 : 2048, coarse ? 1024 : 2048);
space.key.shadow.bias = -0.0004;
space.key.shadow.normalBias = 0.04;
space.key.castShadow = true;

const post = createPost(renderer, { lite: coarse });
post.params.uAberr.value = 0.22;
post.params.uGrain.value = 0.03;
post.params.uBloom.value = 0.9;
post.params.uWarm.value = 0.3;
post.params.uExposure.value = 1.05;

// The hero shot from SentinelSpread's chapter ledger.
const target = new THREE.Vector3(-4.5, -0.5, 4.2);
const home = new THREE.Vector3(33.5, 10.5, 19.5);
const phoneTarget = new THREE.Vector3(0.5, -1.5, 0);

function resize() {
  renderer.setPixelRatio(Math.min(devicePixelRatio, coarse ? 1.25 : 1.5));
  renderer.setSize(innerWidth, innerHeight, false);
  const { width, height } = renderer.getDrawingBufferSize(new THREE.Vector2());
  post.resize(width, height);
  camera.aspect = innerWidth / innerHeight;
  camera.fov = innerWidth < 720 ? 52 : 40;
  camera.updateProjectionMatrix();
}
resize();
addEventListener("resize", resize, { passive: true });

/* Drag-to-rotate turntable with inertia and idle drift. */
const spin = { yaw: 0, pitch: 0, vYaw: 0, vPitch: 0, dragging: false, x: 0, y: 0, idle: 0 };
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
canvas.addEventListener("pointerdown", (e) => {
  spin.dragging = true; spin.x = e.clientX; spin.y = e.clientY; spin.idle = 0;
  canvas.setPointerCapture(e.pointerId); document.body.classList.add("is-dragging");
});
canvas.addEventListener("pointermove", (e) => {
  if (!spin.dragging) return;
  const dx = e.clientX - spin.x, dy = e.clientY - spin.y;
  spin.x = e.clientX; spin.y = e.clientY;
  spin.vYaw = -dx * 0.0055; spin.vPitch = e.pointerType === "touch" ? 0 : dy * 0.004;
  spin.yaw += spin.vYaw; spin.pitch = clamp(spin.pitch + spin.vPitch, -0.55, 0.65);
});
const release = () => { spin.dragging = false; document.body.classList.remove("is-dragging"); };
canvas.addEventListener("pointerup", release);
canvas.addEventListener("pointercancel", release);

/* Effect channels: the same fx object SentinelSpread's chapters drive, set here by buttons. */
const fx = { open: 0, beam: 0.55, holo: 0, audio: 0, boost: 0 };
const goal = { open: 0, beam: 1, holo: 0, audio: 0 };
const buttons = [...document.querySelectorAll("[data-mode]")];
buttons.forEach((b) => b.addEventListener("click", () => {
  for (const k of Object.keys(goal)) goal[k] = k === b.dataset.mode ? 1 : k === "beam" ? 0.2 : 0;
  buttons.forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
}));
const damp = (c, t, l, dt) => c + (t - c) * (1 - Math.exp(-l * dt));

const Y = new THREE.Vector3(0, 1, 0), right = new THREE.Vector3(), pos = new THREE.Vector3();
let ship = null, time = 0, last = 0, first = true;

function frame(now) {
  requestAnimationFrame(frame);
  const dt = last ? Math.min((now - last) / 1000, 1 / 30) : 1 / 60;
  last = now;
  if (!reduce) time += dt;

  if (!spin.dragging) {
    spin.yaw += spin.vYaw * 18 * dt; spin.pitch = clamp(spin.pitch + spin.vPitch * 18 * dt, -0.55, 0.65);
    spin.vYaw *= Math.exp(-3.2 * dt); spin.vPitch *= Math.exp(-3.2 * dt);
    spin.idle += dt;
    if (!reduce && spin.idle > 2.5) spin.yaw += dt * 0.035 * Math.min(1, (spin.idle - 2.5) / 3);
  }
  // phones: centre the station (no side copy to balance) and pull back
  const tgt = innerWidth < 720 ? phoneTarget : target;
  const off = home.clone().sub(target);
  if (innerWidth < 720) off.multiplyScalar(1.45);
  off.applyAxisAngle(Y, spin.yaw);
  right.crossVectors(Y, off).normalize();
  off.applyAxisAngle(right, -spin.pitch);
  pos.copy(tgt).add(off);
  camera.position.copy(pos);
  camera.lookAt(tgt);

  for (const k of Object.keys(goal)) fx[k] = reduce ? goal[k] : damp(fx[k], goal[k], 2.2, dt);
  uniforms.uTime.value = time;
  uniforms.uScale.value = renderer.domElement.height / (2 * Math.tan(THREE.MathUtils.degToRad(camera.fov) / 2));
  ship.update(time, fx);
  space.update(camera);
  post.params.uTime.value = time;
  post.render(scene, camera);
  if (first) { first = false; finishBoot(); }
}

buildShip(scene, renderer, uniforms)
  .then((s) => { ship = s; return renderer.compileAsync ? renderer.compileAsync(scene, camera) : null; })
  .then(() => requestAnimationFrame(frame))
  .catch((err) => { console.error(err); finishBoot(); notice("The station model couldn't load. Serve this folder over http (python3 -m http.server), not file://."); });
