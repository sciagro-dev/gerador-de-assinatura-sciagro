import json, base64, re

AI = 'ai/'
D = json.load(open(AI+'extracted_paths.json'))
with open(AI+'logo_b64.txt') as f: LOGO_B64 = f.read().strip()
with open(AI+'logo_email_b64.txt') as f: LOGO_EMAIL_B64 = f.read().strip()
with open(AI+'leaf_rgba.png','rb') as f: LEAF_B64 = base64.b64encode(f.read()).decode()
with open('html2canvas.js') as f: H2C = f.read()

VIEWBOX = "0.847656 0.472656 497.394532 181.707032"
CARD_W, CARD_H = 497.394532, 181.707032

BLUE = "#104E9D"
GREEN_TITLE = "#8ABE44"
GREEN_ICON = "#85BE56"
TEXT_DARK = "#221E20"
PAPER = "#F5F9FD"
DIVIDER = "#BEE2F7"

LOGO_X, LOGO_Y = 424.194669, 148.1398
LOGO_W, LOGO_H = 1500*0.0461146, 757*0.0459832

# folha: no arquivo .ai original a arte da folha (dentro do PNG 512x512) vaza um
# pouco para fora do círculo — reduzida e recentralizada aqui a pedido do Fabio,
# para caber 100% dentro do círculo (bbox real da arte dentro do PNG: x 63-448,
# y 0-511; círculo: centro (35.59375, 166.376953), raio ~8.008)
LEAF_SCALE = 0.017238
LEAF_ART_CX_PX, LEAF_ART_CY_PX = 255.5, 255.5  # centro do bbox real da arte, em px do PNG 512x512
CIRCLE_CX, CIRCLE_CY = 35.59375, 166.376953
LEAF_X = CIRCLE_CX - LEAF_ART_CX_PX * LEAF_SCALE
LEAF_Y = CIRCLE_CY - LEAF_ART_CY_PX * LEAF_SCALE
LEAF_W = LEAF_H = 512 * LEAF_SCALE

def wave_stroke_transformed():
    m = re.search(r'matrix\(([^)]*)\)', D['wave_stroke']['transform'])
    a,b,c,dd,e,f = [float(x) for x in m.group(1).split(',')]
    def tx(x,y):
        return (a*x + c*y + e, b*x + dd*y + f)
    d = D['wave_stroke']['d']
    tokens = re.findall(r'[MLCZ]|-?\d+\.?\d*', d)
    out = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in ('M','L'):
            x,y = float(tokens[i+1]), float(tokens[i+2])
            X,Y = tx(x,y)
            out.append(f"{t} {X:.3f},{Y:.3f}")
            i += 3
        elif t == 'C':
            nums = [float(n) for n in tokens[i+1:i+7]]
            pts = [tx(nums[0],nums[1]), tx(nums[2],nums[3]), tx(nums[4],nums[5])]
            out.append("C " + " ".join(f"{x:.3f},{y:.3f}" for x,y in pts))
            i += 7
        elif t == 'Z':
            out.append("Z")
            i += 1
        else:
            i += 1
    return " ".join(out)

WAVE_STROKE_D = wave_stroke_transformed()

CARD_SVG = f"""<svg id="card-svg" viewBox="{VIEWBOX}" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" style="display:block;" preserveAspectRatio="none">
            <defs>
              <clipPath id="cardClip">
                <path d="{D['card_base']['d']}"/>
              </clipPath>
              <clipPath id="photoClip">
                <path d="{WAVE_STROKE_D}"/>
              </clipPath>
            </defs>
            <g clip-path="url(#cardClip)">
              <rect x="0.847656" y="0.472656" width="{CARD_W}" height="{CARD_H}" fill="#ffffff"/>
              <image id="photo-img" x="0.847656" y="0.472656" width="{CARD_W}" height="{CARD_H}" preserveAspectRatio="none" href="" style="display:none;" clip-path="url(#photoClip)"/>
              <text id="photo-initials" x="88" y="98" font-family="Sora, sans-serif" font-size="46" font-weight="600" fill="#ffffff" opacity="0.85" text-anchor="middle" clip-path="url(#photoClip)" style="display:none;"></text>
              <!-- sem foto escolhida: mostra a logo da SCI-AGRO no lugar, em vez de deixar a área vazia -->
              <image id="no-photo-logo" x="20" y="58.5" width="130" height="65.6" href="data:image/png;base64,{LOGO_B64}"/>

              <path d="{D['panel']['d']}" fill="{PAPER}"/>
              <path d="{D['bar']['d']}" fill="{BLUE}"/>
              <path d="{D['ribbon']['d']}" fill="{GREEN_TITLE}"/>
              <path d="{WAVE_STROKE_D}" fill="none" stroke="{BLUE}" stroke-width="1.1" stroke-linecap="round"/>

              <path d="{D['divider1']['d']}" fill="{DIVIDER}"/>
              <path d="{D['divider2']['d']}" fill="{DIVIDER}"/>
              <path d="{D['divider3']['d']}" fill="{DIVIDER}"/>

              <path d="{D['circle_phone']['d']}" fill="{GREEN_ICON}"/>
              <path d="{D['glyph_phone_1']['d']}" fill="#ffffff"/>
              <path d="{D['circle_email']['d']}" fill="{GREEN_ICON}"/>
              <path d="{D['glyph_email_1']['d']}" fill="#ffffff"/>
              <path d="{D['glyph_email_2']['d']}" fill="#ffffff"/>
              <path d="{D['circle_site']['d']}" fill="{GREEN_ICON}"/>
              <path d="{D['glyph_site_1']['d']}" fill="#ffffff"/>
              <path d="{D['glyph_site_2']['d']}" fill="#ffffff"/>
              <path d="{D['circle_address']['d']}" fill="{GREEN_ICON}"/>
              <path d="{D['glyph_addr_1']['d']}" fill="#ffffff"/>
              <path d="{D['glyph_addr_2']['d']}" fill="#ffffff"/>

              <path d="{D['leaf_circle']['d']}" fill="{PAPER}"/>
              <image x="{LEAF_X}" y="{LEAF_Y}" width="{LEAF_W}" height="{LEAF_H}" href="data:image/png;base64,{LEAF_B64}"/>
              <image id="logo-img" x="{LOGO_X}" y="{LOGO_Y}" width="{LOGO_W}" height="{LOGO_H}" href="data:image/png;base64,{LOGO_B64}"/>

              <text id="ov-nome" x="233.676143" y="36.289978" font-family="Sora, sans-serif" font-size="14.2" font-weight="700" fill="{BLUE}">Nome aqui</text>
              <text id="ov-cargo" x="233.676143" y="51.402539" font-family="Sora, sans-serif" font-size="10.15" font-weight="400" fill="{GREEN_TITLE}">Cargo Aqui</text>

              <text id="ov-tel" x="260.2" y="76.661992" font-family="Sora, sans-serif" font-size="8.2" font-weight="600" fill="{TEXT_DARK}">Telefone</text>
              <text id="ov-email" x="260.2" y="103.236972" font-family="Sora, sans-serif" font-size="8.2" font-weight="600" fill="{TEXT_DARK}">email</text>
              <text x="260.2" y="130.47964" font-family="Sora, sans-serif" font-size="8.2" font-weight="600" fill="{TEXT_DARK}">sci-agro.com.br</text>
              <text x="260.2" y="150.617521" font-family="Sora, sans-serif" font-size="8.0" font-weight="600" fill="{TEXT_DARK}">Via Vicente Verdi, 835</text>
              <text x="260.2" y="160.748232" font-family="Sora, sans-serif" font-size="8.0" font-weight="600" fill="{TEXT_DARK}">Bairro Industrial &#8211; CEP 13518-070</text>
              <text x="260.2" y="170.878944" font-family="Sora, sans-serif" font-size="8.0" font-weight="600" fill="{TEXT_DARK}">Charqueada &#8211; SP</text>

              <text x="49.70821" y="170.702736" font-family="Sora, sans-serif" font-size="8.0" font-weight="600" fill="#ffffff">Your Product. Our Responsibility.</text>
            </g>
          </svg>"""

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Gerador de Assinatura de E-mail — SCI-AGRO</title>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  :root{
    --blue:#104E9D;
    --green-title:#8ABE44;
    --green-icon:#85BE56;
    --paper:#F5F9FD;
    --ink:#221E20;
  }
  *{box-sizing:border-box;}
  body{
    margin:0;
    font-family:'Segoe UI', Arial, Helvetica, sans-serif;
    background:#eef1f5;
    color:#20242b;
    padding:32px 16px 64px;
  }
  .wrap{ max-width:1160px; margin:0 auto; }
  h1{ font-size:22px; margin:0 0 4px; color:var(--blue); }
  .sub{ color:#5b6270; font-size:14px; margin:0 0 28px; }
  .grid{
    display:grid;
    grid-template-columns: 360px 1fr;
    gap:28px;
    align-items:start;
  }
  @media (max-width: 900px){ .grid{grid-template-columns: 1fr;} }
  .panel{
    background:#fff;
    border-radius:12px;
    padding:22px 22px 26px;
    box-shadow:0 1px 3px rgba(20,30,60,.08), 0 1px 2px rgba(20,30,60,.06);
  }
  .panel h2{ font-size:15px; margin:0 0 16px; color:var(--blue); }
  label{
    display:block; font-size:12.5px; font-weight:600;
    color:#3a4150; margin:14px 0 5px;
  }
  label:first-of-type{margin-top:0;}
  input[type=text], input[type=tel], input[type=email]{
    width:100%; padding:9px 11px; border:1px solid #d7dbe3;
    border-radius:7px; font-size:13.5px; font-family:inherit;
    color:#20242b; background:#fbfcfe;
  }
  input:focus{ outline:none; border-color:var(--blue); background:#fff; }
  .photo-row{ display:flex; align-items:center; gap:14px; margin-top:6px; }
  .photo-preview-mini{
    width:52px;height:40px;border-radius:8px;
    object-fit:cover; border:2px solid #e2e6ee; background:#f1f3f7;
  }
  .file-btn{
    display:inline-block; padding:8px 14px; background:var(--blue);
    color:#fff; border-radius:7px; font-size:13px; font-weight:600;
    cursor:pointer; border:none;
  }
  .file-btn:hover{background:#0c3b78;}
  input[type=file]{display:none;}
  .hint{ font-size:11.5px; color:#8a90a0; margin-top:4px; }
  .fixed-note{
    font-size:11.5px; color:#8a90a0; background:#f4f6fa; border:1px dashed #d7dbe3;
    border-radius:7px; padding:8px 10px; margin-top:4px; line-height:1.5;
  }
  .photo-controls{ display:none; margin-top:12px; }
  .photo-controls.show{ display:block; }
  .photo-controls .zoom-row{ display:flex; align-items:center; gap:10px; }
  .photo-controls input[type=range]{ flex:1; accent-color:var(--blue); }
  .photo-controls .reset-btn{
    margin-top:8px; background:none; border:1px solid #d7dbe3; color:var(--blue);
    font-size:12px; font-weight:600; padding:6px 12px; border-radius:6px; cursor:pointer;
  }
  .photo-controls .reset-btn:hover{ background:#f1f5fb; }
  .export-btn{
    width:100%; margin-top:22px; padding:13px; background:var(--green-icon);
    color:#fff; border:none; border-radius:8px; font-size:14.5px;
    font-weight:700; cursor:pointer; letter-spacing:.2px;
  }
  .export-btn:hover{background:#6ba33f;}
  .export-btn:disabled{opacity:.6; cursor:default;}
  .export-btn.secondary{
    background:#fff; border:1.5px solid var(--blue); color:var(--blue); margin-top:10px;
  }
  .export-btn.secondary:hover{ background:#f1f5fb; }
  .html-output{ display:none; margin-top:14px; }
  .html-output.show{ display:block; }
  .html-output textarea{
    width:100%; height:150px; font-family:'SFMono-Regular',Consolas,monospace;
    font-size:11px; padding:10px; border:1px solid #d7dbe3; border-radius:7px;
    resize:vertical; color:#3a4150; background:#fbfcfe;
  }
  .preview-outer{ overflow:auto; padding:4px; }
  .preview-scale-wrap{ width:900px; height:328.9px; }
  #signature-card{
    position:relative;
    width:1500px;
    height:547.9px;
    background:#fff;
    border-radius:38.5px;
    overflow:hidden;
    transform:scale(0.6);
    transform-origin:top left;
    box-shadow:0 0 0 1px #e3e8f0;
    touch-action:none;
    cursor:grab;
  }
  #signature-card.dragging{ cursor:grabbing; }
  #signature-card svg, #signature-card img{ -webkit-user-drag:none; user-select:none; -webkit-user-select:none; }
</style>
</head>
<body>
<div class="wrap">
  <h1>Gerador de assinatura de e-mail — SCI-AGRO</h1>
  <p class="sub">Preencha seus dados, confira a pré-visualização ao lado e exporte a assinatura como imagem PNG ou como código HTML.</p>

  <div class="grid">
    <div class="panel">
      <h2>Seus dados</h2>

      <label for="f-foto">Foto</label>
      <div class="photo-row">
        <img id="mini-preview" class="photo-preview-mini" src="" alt="">
        <label class="file-btn" for="f-foto">Escolher foto</label>
        <input type="file" id="f-foto" accept="image/*">
      </div>
      <div class="hint" id="photo-hint">Prefira uma foto horizontal, com o rosto no terço esquerdo — a moldura é recortada em formato de onda.</div>
      <div class="photo-controls" id="photo-controls">
        <div class="hint">Arraste a foto na pré-visualização ou use os controles abaixo para posicionar e ajustar o enquadramento.</div>
        <div class="zoom-row">
          <span class="hint" style="margin:0;">Zoom</span>
          <input type="range" id="f-zoom" min="1" max="3" step="0.01" value="1">
        </div>
        <div class="zoom-row">
          <span class="hint" style="margin:0;">Horizontal</span>
          <input type="range" id="f-panx" min="-100" max="100" step="1" value="0">
        </div>
        <div class="zoom-row">
          <span class="hint" style="margin:0;">Vertical</span>
          <input type="range" id="f-pany" min="-100" max="100" step="1" value="0">
        </div>
        <button type="button" class="reset-btn" id="btn-reset-photo">Centralizar</button>
      </div>

      <label for="f-nome">Nome</label>
      <input type="text" id="f-nome" placeholder="">
      <div class="hint">Use só nome e sobrenome (ex: João Silva) — nomes muito longos ficam menores para caber.</div>

      <label for="f-cargo">Cargo / Área</label>
      <input type="text" id="f-cargo" placeholder="Ex: Marketing">

      <label for="f-cargo-en">Cargo / Área (inglês)</label>
      <input type="text" id="f-cargo-en" placeholder="Preenchido automaticamente…">
      <div class="hint" id="cargo-en-hint">Traduzido automaticamente — não sabe a tradução? Pode deixar como está, ou editar se quiser ajustar.</div>

      <label for="f-tel">Telefone</label>
      <input type="tel" id="f-tel" placeholder="">

      <label for="f-email">E-mail</label>
      <input type="email" id="f-email" placeholder="">

      <label>Site</label>
      <div class="fixed-note">sci-agro.com.br — fixo para todos os colaboradores.</div>

      <label>Endereço</label>
      <div class="fixed-note">Via Vicente Verdi, 835 — Bairro Industrial — CEP 13518-070 — Charqueada – SP<br>Fixo para todos os colaboradores.</div>

      <button class="export-btn" id="btn-export">Baixar assinatura em PNG</button>
      <button class="export-btn secondary" id="btn-export-html">Gerar código HTML da assinatura</button>
      <div class="html-output" id="html-output">
        <div class="hint" style="margin-top:0;">Cole este código na opção "Editar em HTML" do seu cliente de e-mail (Gmail, Outlook, etc). A foto e o logo já vêm embutidos na assinatura.</div>
        <textarea id="html-code" readonly></textarea>
        <button type="button" class="reset-btn" id="btn-copy-html" style="margin-top:8px;">Copiar código</button>
      </div>
    </div>

    <div class="panel">
      <h2>Pré-visualização</h2>
      <div class="preview-outer">
        <div class="preview-scale-wrap">
        <div id="signature-card">
          __CARD_SVG__
        </div>
        </div>
      </div>
      <div class="hint" style="margin-top:10px;">A assinatura é exportada exatamente como aparece aqui, em alta resolução — o traço da onda e os ícones vêm direto da arte original em vetor.</div>
    </div>
  </div>
</div>

<script>
const $ = id => document.getElementById(id);
const NS = 'http://www.w3.org/2000/svg';
const LOGO_EMAIL_URL = 'data:image/png;base64,__LOGO_EMAIL_B64__';

function initials(name){
  const parts = name.trim().split(/\\s+/).filter(Boolean);
  if(parts.length === 0) return '';
  if(parts.length === 1) return parts[0][0].toUpperCase();
  return (parts[0][0] + parts[parts.length-1][0]).toUpperCase();
}

// autoajuste de texto em <text> SVG: encolhe font-size até caber em maxWidth (unidades do viewBox)
const FIELD_MAX_FONT = {};
function autoFitSvgText(el, fullText, maxWidth){
  if(!(el.id in FIELD_MAX_FONT)) FIELD_MAX_FONT[el.id] = parseFloat(el.getAttribute('font-size'));
  const maxSize = FIELD_MAX_FONT[el.id];
  const minSize = maxSize * 0.55;
  let size = maxSize;
  el.textContent = fullText;
  el.setAttribute('font-size', size);
  while (el.getComputedTextLength() > maxWidth && size > minSize) {
    size -= 0.1;
    el.setAttribute('font-size', size);
  }
  if (el.getComputedTextLength() > maxWidth) {
    let text = fullText;
    while (text.length > 1 && el.getComputedTextLength() > maxWidth) {
      text = text.slice(0, -1);
      el.textContent = text.trimEnd() + '…';
    }
  }
}

function bind(inputId, elId, fallback, maxWidth){
  const input = $(inputId);
  const el = $(elId);
  const update = () => autoFitSvgText(el, input.value.trim() || fallback, maxWidth);
  input.addEventListener('input', update);
  update();
}

// ---- tradução automática do cargo/área (PT → EN) ----
// para quem não sabe a tradução: preenche sozinho um rascunho ao digitar em
// português; a pessoa pode editar ou deixar como está. Funciona offline com um
// dicionário de termos comuns de cargo/departamento e, se houver internet, tenta
// melhorar o resultado com um serviço de tradução gratuito (best-effort).
function stripAccents(s){
  return s.normalize('NFD').replace(/[\\u0300-\\u036f]/g, '');
}
function normCargo(s){
  return stripAccents(s.toLowerCase().trim()).replace(/\\s+/g, ' ');
}

// dicionário de departamentos/cargos: construído a partir das assinaturas reais
// já usadas na SCI-AGRO (lidas de uma pasta compartilhada pelo Fabio), então
// reflete a terminologia que a empresa já usa — não é uma tradução genérica.
const CARGO_PHRASES = {
  'rh': 'Human Resources',
  'recursos humanos': 'Human Resources',
  'toxicologia in vivo': 'Toxicology In Vivo',
  'toxicologia in vitro': 'Toxicology In Vitro',
  'almoxarifado': 'Stockroom',
  'projetos': 'Projects',
  'fisico-quimica': 'Physical-Chemical',
  'fisico quimica': 'Physical-Chemical',
  'comercial': 'Sales',
  'microbiologia': 'Microbiology',
  'entomologia': 'Entomology',
  'ecotoxicologia': 'Ecotoxicology',
  'gerente comercial': 'Sales Manager',
  'gerente fisico-quimica': 'Physical-Chemical Manager',
  'gerente fisico quimica': 'Physical-Chemical Manager',
  'compras': 'Purchasing Department',
  'gerente ecotoxicologia': 'Ecotoxicology Manager',
  'financeiro': 'Finance Department',
  'diretor de operacoes': 'Chief Operating Officer',
  'diretora de operacoes': 'Chief Operating Officer',
  'importacoes': 'Import',
  'mutagenicidade': 'Mutagenicity',
  'diretora comercial': 'Sales Director',
  'diretor comercial': 'Sales Director',
  'vice presidente': 'Vice President',
  'nf': 'Invoice',
  'residuos': 'Residues',
  'garantia de qualidade': 'Quality Assurance',
  'garantia da qualidade': 'Quality Assurance',
  'presidente': 'Chief Executive Officer',
  'gerente de projetos': 'Projects Manager',
  'recepcao': 'Front Desk',
  'recepcao amostras': 'Samples Reception',
  'administrativo': 'Administration',
  'padroes analiticos': 'Analytical Standards',
  'gerente toxicologia & microbiologia': 'Toxicology and Microbiology Manager',
  'gerente toxicologia e microbiologia': 'Toxicology and Microbiology Manager',
  'meio ambiente': 'Environment',
  'assuntos regulatorios': 'Regulatory Affairs',
  'regulatorio': 'Regulatory Affairs',
  'registro': 'Regulatory Affairs',
  'cadeia de suprimentos': 'Supply Chain',
  'pesquisa e desenvolvimento': 'Research and Development',
  'p&d': 'R&D',
  'atendimento ao cliente': 'Customer Service',
  'sucesso do cliente': 'Customer Success',
  'vendas tecnicas': 'Technical Sales',
  'seguranca do trabalho': 'Occupational Safety',
  'comunicacao institucional': 'Institutional Communications',
  'tecnologia da informacao': 'Information Technology',
  'controle de qualidade': 'Quality Control',
};

const CARGO_WORDS = {
  'marketing': 'Marketing', 'vendas': 'Sales', 'comercial': 'Sales',
  'financeiro': 'Finance', 'financas': 'Finance', 'ti': 'IT',
  'tecnologia': 'Technology', 'informacao': 'Information', 'qualidade': 'Quality',
  'producao': 'Production', 'logistica': 'Logistics', 'juridico': 'Legal',
  'diretoria': 'Board of Directors', 'diretor': 'Director', 'diretora': 'Director',
  'gerente': 'Manager', 'gerencia': 'Management', 'coordenador': 'Coordinator',
  'coordenadora': 'Coordinator', 'coordenacao': 'Coordination',
  'supervisor': 'Supervisor', 'supervisora': 'Supervisor', 'analista': 'Analyst',
  'assistente': 'Assistant', 'auxiliar': 'Assistant', 'estagiario': 'Intern',
  'estagiaria': 'Intern', 'especialista': 'Specialist', 'consultor': 'Consultant',
  'consultora': 'Consultant', 'tecnico': 'Technician', 'tecnica': 'Technician',
  'representante': 'Representative', 'executivo': 'Executive',
  'executiva': 'Executive', 'atendimento': 'Service', 'cliente': 'Customer',
  'clientes': 'Customers', 'compras': 'Purchasing', 'operacoes': 'Operations',
  'administrativo': 'Administration', 'administrativa': 'Administration',
  'contabilidade': 'Accounting', 'controladoria': 'Controllership',
  'manutencao': 'Maintenance', 'seguranca': 'Safety', 'trabalho': 'Work',
  'ambiente': 'Environment', 'assistencia': 'Assistance', 'pesquisa': 'Research',
  'desenvolvimento': 'Development', 'suprimentos': 'Supply', 'cadeia': 'Chain',
  'projetos': 'Projects', 'projeto': 'Project', 'engenharia': 'Engineering',
  'comunicacao': 'Communications', 'institucional': 'Institutional',
  'eventos': 'Events', 'digital': 'Digital', 'conteudo': 'Content',
  'design': 'Design', 'criativo': 'Creative', 'planejamento': 'Planning',
  'toxicologia': 'Toxicology', 'microbiologia': 'Microbiology',
  'ecotoxicologia': 'Ecotoxicology', 'entomologia': 'Entomology',
  'mutagenicidade': 'Mutagenicity', 'residuos': 'Residues',
  'recepcao': 'Front Desk', 'almoxarifado': 'Stockroom',
  'importacoes': 'Import', 'presidente': 'President',
  'area': 'Area', 'e': 'and', 'de': 'of', 'do': 'of', 'da': 'of', 'dos': 'of',
  'das': 'of',
};

// para "Gerente X" / "Diretor(a) X" sem correspondência exata: monta o padrão
// que a SCI-AGRO usa de verdade (departamento em inglês + cargo no final —
// ex.: "Ecotoxicology Manager", não "Manager of Ecotoxicology").
function tryRoleDeptPattern(norm){
  const m = norm.match(/^(gerente|diretor|diretora)( de| do| da)? (.+)$/);
  if (!m) return null;
  const role = m[1];
  const deptRaw = m[3];
  const dept = CARGO_WORDS[deptRaw] || CARGO_PHRASES[deptRaw];
  if (!dept) return null;
  const roleEn = role === 'gerente' ? 'Manager' : 'Director';
  return `${dept} ${roleEn}`;
}

function dictTranslateCargo(pt){
  const norm = normCargo(pt);
  if (!norm) return '';
  if (CARGO_PHRASES[norm]) return CARGO_PHRASES[norm];
  const patterned = tryRoleDeptPattern(norm);
  if (patterned) return patterned;
  const words = norm.split(' ');
  const translated = words.map(w => CARGO_WORDS[w] || w);
  return translated
    .map((w, i) => (w === 'and' || w === 'of') ? w : (w.charAt(0).toUpperCase() + w.slice(1)))
    .join(' ');
}

let cargoEnTouched = $('f-cargo-en').value.trim() !== '';
let cargoTranslateTimer = null;

async function liveTranslateCargo(text){
  try{
    const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(text)}&langpair=pt|en`;
    const resp = await fetch(url, {signal: AbortSignal.timeout(4000)});
    if(!resp.ok) return null;
    const data = await resp.json();
    const t = data && data.responseData && data.responseData.translatedText;
    const quality = data && data.responseData && data.responseData.match;
    if (t && (!quality || quality > 0.3)) return t;
  }catch(e){ /* offline ou serviço indisponível — mantém a sugestão do dicionário */ }
  return null;
}

function autoTranslateCargo(){
  const pt = $('f-cargo').value.trim();
  if (cargoEnTouched || !pt) return;
  const guess = dictTranslateCargo(pt);
  setCargoEnValue(guess);
  clearTimeout(cargoTranslateTimer);
  cargoTranslateTimer = setTimeout(async () => {
    if (cargoEnTouched || $('f-cargo').value.trim() !== pt) return;
    const live = await liveTranslateCargo(pt);
    if (live && !cargoEnTouched && $('f-cargo').value.trim() === pt){
      setCargoEnValue(live);
    }
  }, 500);
}

// altera o campo EN por código (tradução automática) sem marcar como "editado
// manualmente" e sem disparar o listener de tradução — só atualiza o preview.
function setCargoEnValue(value){
  $('f-cargo-en').value = value;
  updateCargoSvg();
}

$('f-cargo-en').addEventListener('input', () => {
  cargoEnTouched = $('f-cargo-en').value.trim() !== '';
  updateCargoSvg();
});
$('f-cargo').addEventListener('input', () => {
  autoTranslateCargo();
  updateCargoSvg();
});

function cargoTexto(){
  const pt = $('f-cargo').value.trim();
  const en = $('f-cargo-en').value.trim();
  if (pt && en) return `${pt} | ${en}`;
  return pt || en || 'Cargo Aqui';
}

function updateCargoSvg(){
  autoFitSvgText($('ov-cargo'), cargoTexto(), 248);
}

bind('f-nome','ov-nome','Nome aqui', 248);
updateCargoSvg();
autoTranslateCargo();
bind('f-tel','ov-tel','Telefone', 220);
bind('f-email','ov-email','email', 220);

$('f-nome').addEventListener('input', () => {
  $('photo-initials').textContent = initials($('f-nome').value);
});

// ---- posicionamento da foto: arrastar ou usar os controles para mover/ampliar ----
// canvas interno em alta resolução, na MESMA proporção do cartão inteiro (497.4 x 181.7) —
// não precisa de recorte em onda no canvas: o SVG por cima (painel + faixa) já esconde
// tudo que não deve aparecer, deixando a foto visível só na área em formato de onda.
const PHOTO_W = 2200, PHOTO_H = Math.round(2200 * (181.707032/497.394532));
const BOX_W = 497.394532, BOX_H = 181.707032; // tamanho do cartão no viewBox do SVG

// a foto só fica visível na faixa em onda à esquerda do cartão (medido no arquivo
// original: no máximo ~47% da largura do cartão, um pouco antes da faixa azul) — o
// resto do canvas fica escondido atrás do painel/faixa. O ajuste de zoom/posição
// precisa "encaixar" (cover) a foto nessa janela visível, não no cartão inteiro:
// encaixar no cartão inteiro (bem mais largo que alto) sempre força a largura como
// referência e zera a folga horizontal, por isso o slider horizontal não fazia nada.
const VISIBLE_W = PHOTO_W * 0.48;

// "cover" no ajuste mínimo sempre deixa UM dos dois eixos (o que estiver mais perto
// da proporção da janela) sem folga nenhuma pra arrastar — com uma foto na vertical
// (retrato), por exemplo, é a largura que fica travada em 0, e dá a impressão de que
// "a foto não sai da margem" no horizontal. Multiplicar a escala mínima por uma folga
// extra (bem além do estritamente necessário pra cobrir) garante que os dois eixos
// sempre tenham espaço pra arrastar e centralizar a foto à vontade, não só o que por
// acaso sobra mais largo/alto que a foto.
const PAN_OVERSCAN = 1.3;

const photoCanvas = document.createElement('canvas');
photoCanvas.width = PHOTO_W;
photoCanvas.height = PHOTO_H;
const photoCtx = photoCanvas.getContext('2d');

let originalPhoto = null;
let photoZoom = 1;
let photoFracX = 0;
let photoFracY = 0;

function getMaxPan(){
  const baseScale = Math.max(VISIBLE_W / originalPhoto.width, PHOTO_H / originalPhoto.height) * PAN_OVERSCAN;
  const eff = baseScale * photoZoom;
  const dw = originalPhoto.width * eff;
  const dh = originalPhoto.height * eff;
  return {
    dw, dh,
    maxPanX: Math.max(0, (dw - VISIBLE_W) / 2),
    maxPanY: Math.max(0, (dh - PHOTO_H) / 2),
  };
}

function renderPhoto(){
  if(!originalPhoto) return;
  photoFracX = Math.max(-1, Math.min(1, photoFracX));
  photoFracY = Math.max(-1, Math.min(1, photoFracY));
  const { dw, dh, maxPanX, maxPanY } = getMaxPan();
  // sinal invertido no X: arrastar/deslizar para a direita deve revelar o lado
  // direito da foto (mover a "janela" pra direita), não o esquerdo.
  const dx = (VISIBLE_W - dw) / 2 - maxPanX * photoFracX;
  const dy = (PHOTO_H - dh) / 2 + maxPanY * photoFracY;

  photoCtx.clearRect(0, 0, PHOTO_W, PHOTO_H);
  photoCtx.drawImage(originalPhoto, dx, dy, dw, dh);

  const url = photoCanvas.toDataURL('image/png');
  $('photo-img').setAttribute('href', url);
  $('photo-img').style.display = 'block';
  $('photo-initials').style.display = 'none';
  $('no-photo-logo').style.display = 'none';
  $('mini-preview').src = url;

  $('f-panx').value = Math.round(photoFracX * 100);
  $('f-pany').value = Math.round(photoFracY * 100);
}

function resetPhotoPosition(){
  photoZoom = 1;
  photoFracX = 0;
  photoFracY = 0;
  $('f-zoom').value = 1;
  $('f-panx').value = 0;
  $('f-pany').value = 0;
  renderPhoto();
}

$('f-foto').addEventListener('change', (e) => {
  const file = e.target.files[0];
  if(!file) return;
  const reader = new FileReader();
  reader.onload = (ev) => {
    const img = new Image();
    img.onload = () => {
      originalPhoto = img;
      $('photo-controls').classList.add('show');
      resetPhotoPosition();
    };
    img.src = ev.target.result;
  };
  reader.readAsDataURL(file);
});

$('f-zoom').addEventListener('input', (e) => { photoZoom = parseFloat(e.target.value); renderPhoto(); });
$('f-panx').addEventListener('input', (e) => { photoFracX = parseFloat(e.target.value) / 100; renderPhoto(); });
$('f-pany').addEventListener('input', (e) => { photoFracY = parseFloat(e.target.value) / 100; renderPhoto(); });
$('btn-reset-photo').addEventListener('click', resetPhotoPosition);

(function(){
  const el = $('signature-card');
  el.addEventListener('dragstart', (e) => e.preventDefault());
  el.addEventListener('selectstart', (e) => e.preventDefault());

  let dragging = false;
  let startX = 0, startY = 0, startFracX = 0, startFracY = 0;
  // a pré-visualização é exibida a 0.6x; corrige a razão para converter px de tela em px do canvas interno
  const ratioX = PHOTO_W / (BOX_W * 0.6), ratioY = PHOTO_H / (BOX_H * 0.6);

  el.addEventListener('pointerdown', (e) => {
    if(!originalPhoto) return;
    e.preventDefault();
    dragging = true;
    startX = e.clientX; startY = e.clientY;
    startFracX = photoFracX; startFracY = photoFracY;
    el.classList.add('dragging');
    el.setPointerCapture(e.pointerId);
  });
  el.addEventListener('pointermove', (e) => {
    if(!dragging) return;
    e.preventDefault();
    const { maxPanX, maxPanY } = getMaxPan();
    const deltaPxX = (e.clientX - startX) * ratioX;
    const deltaPxY = (e.clientY - startY) * ratioY;
    // arrastar com o mouse é "pegar e mover a foto": puxar pra direita tem que
    // levar a foto pra direita (o oposto do sentido do slider, que representa a
    // "janela" se movendo, não a foto) — por isso o sinal de X aqui é invertido
    // em relação ao slider, enquanto o de Y já nasceu certo.
    photoFracX = startFracX - (maxPanX > 0 ? deltaPxX / maxPanX : 0);
    photoFracY = startFracY + (maxPanY > 0 ? deltaPxY / maxPanY : 0);
    renderPhoto();
  });
  const endDrag = () => {
    if(!dragging) return;
    dragging = false;
    el.classList.remove('dragging');
  };
  el.addEventListener('pointerup', endDrag);
  el.addEventListener('pointercancel', endDrag);
  el.addEventListener('pointerleave', endDrag);
})();

const EXPORT_WIDTH = 1800;

function downscaleCanvas(srcCanvas, targetWidth){
  let current = srcCanvas;
  let currentWidth = srcCanvas.width;
  let currentHeight = srcCanvas.height;
  while (currentWidth > targetWidth * 2) {
    const nextWidth = Math.round(currentWidth / 2);
    const nextHeight = Math.round(currentHeight / 2);
    const step = document.createElement('canvas');
    step.width = nextWidth;
    step.height = nextHeight;
    const stepCtx = step.getContext('2d');
    stepCtx.imageSmoothingEnabled = true;
    stepCtx.imageSmoothingQuality = 'high';
    stepCtx.drawImage(current, 0, 0, nextWidth, nextHeight);
    current = step;
    currentWidth = nextWidth;
    currentHeight = nextHeight;
  }
  const targetHeight = Math.round(targetWidth * (srcCanvas.height / srcCanvas.width));
  const out = document.createElement('canvas');
  out.width = targetWidth;
  out.height = targetHeight;
  const outCtx = out.getContext('2d');
  outCtx.imageSmoothingEnabled = true;
  outCtx.imageSmoothingQuality = 'high';
  outCtx.drawImage(current, 0, 0, targetWidth, targetHeight);
  return out;
}

function fileNome(){
  return ($('f-nome').value.trim() || 'assinatura').toLowerCase().replace(/\\s+/g,'-').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
}

async function saveFile(filename, blob){
  try{
    if (window.claude && typeof window.claude.use === 'function'){
      const downloads = await window.claude.use('downloads');
      if (downloads){
        await downloads.save({filename, data: blob});
        return true;
      }
    }
  }catch(e){ /* sem capacidade disponível ou recusado: cai no download clássico */ }
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.download = filename;
  link.href = url;
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 4000);
  return true;
}

$('btn-export').addEventListener('click', () => {
  const btn = $('btn-export');
  btn.disabled = true;
  btn.textContent = 'Gerando imagem…';
  const card = $('signature-card');
  const previousTransform = card.style.transform;
  card.style.transform = 'none';
  html2canvas(card, {scale: 4, backgroundColor: '#ffffff', useCORS: true}).then(bigCanvas => {
    card.style.transform = previousTransform;
    const outCanvas = downscaleCanvas(bigCanvas, EXPORT_WIDTH);
    outCanvas.toBlob(async (blob) => {
      try{
        await saveFile(`assinatura-${fileNome()}.png`, blob);
      }catch(e){ /* usuário cancelou o salvamento — sem erro a mostrar */ }
      btn.disabled = false;
      btn.textContent = 'Baixar assinatura em PNG';
    }, 'image/png');
  }).catch(() => {
    btn.disabled = false;
    btn.textContent = 'Baixar assinatura em PNG';
  });
});

// ---- exportação em HTML (versão simplificada, segura para clientes de e-mail) ----
function fotoThumbDataUrl(){
  // recorta um quadrado à esquerda do canvas de alta resolução da foto e reduz
  // para um tamanho leve (JPEG), já que no HTML de e-mail ela aparece só a 90x90px —
  // embutir a foto em 2200px de largura deixaria o e-mail com vários MB.
  if (!originalPhoto) return '';
  const side = PHOTO_H; // altura do canvas = lado do recorte quadrado (canto esquerdo)
  const thumb = document.createElement('canvas');
  const THUMB_SIZE = 180;
  thumb.width = THUMB_SIZE;
  thumb.height = THUMB_SIZE;
  const tctx = thumb.getContext('2d');
  tctx.imageSmoothingEnabled = true;
  tctx.imageSmoothingQuality = 'high';
  tctx.drawImage(photoCanvas, 0, 0, side, side, 0, 0, THUMB_SIZE, THUMB_SIZE);
  return thumb.toDataURL('image/jpeg', 0.85);
}

function buildSignatureHtml(){
  const nome = $('f-nome').value.trim() || 'Nome Sobrenome';
  const cargo = cargoTexto();
  const tel = $('f-tel').value.trim();
  const email = $('f-email').value.trim();
  const fotoSrc = $('photo-img').style.display !== 'none' ? fotoThumbDataUrl() : '';
  const logoSrc = LOGO_EMAIL_URL;

  // sem foto: mostra a logo da SCI-AGRO no lugar (em vez de uma caixa vazia), num
  // fundo claro — centralizada com atributos de tabela (align/valign), não flexbox,
  // porque o Outlook de mesa (motor do Word) não renderiza flexbox em e-mail.
  const fotoCell = fotoSrc
    ? `<img src="${fotoSrc}" width="90" height="90" alt="${nome}" style="display:block;border-radius:10px;object-fit:cover;width:90px;height:90px;">`
    : `<table cellpadding="0" cellspacing="0" border="0" width="90" height="90" style="width:90px;height:90px;background:#F5F9FD;border-radius:10px;"><tr><td align="center" valign="middle"><img src="${logoSrc}" width="70" alt="SCI-AGRO" style="display:block;max-width:70px;"></td></tr></table>`;

  const linhas = [];
  if (tel) linhas.push(`<tr><td style="padding:2px 0;font:600 13px Arial,sans-serif;color:${'#221E20'};">${tel}</td></tr>`);
  if (email) linhas.push(`<tr><td style="padding:2px 0;font:600 13px Arial,sans-serif;color:${'#221E20'};"><a href="mailto:${email}" style="color:#221E20;text-decoration:none;">${email}</a></td></tr>`);
  linhas.push(`<tr><td style="padding:2px 0;font:600 13px Arial,sans-serif;color:#221E20;"><a href="https://sci-agro.com.br" style="color:#221E20;text-decoration:none;">sci-agro.com.br</a></td></tr>`);
  linhas.push(`<tr><td style="padding:6px 0 0;font:600 12px Arial,sans-serif;color:#221E20;line-height:1.5;">Via Vicente Verdi, 835 — Bairro Industrial<br>CEP 13518-070 — Charqueada – SP</td></tr>`);

  return `<table cellpadding="0" cellspacing="0" border="0" style="font-family:Arial,sans-serif;border-collapse:collapse;">
  <tr>
    <td style="padding:0 18px 0 0;vertical-align:top;border-right:3px solid #104E9D;">${fotoCell}</td>
    <td style="padding:0 18px 0 18px;vertical-align:top;border-right:1px solid #BEE2F7;">
      <table cellpadding="0" cellspacing="0" border="0">
        <tr><td style="font:700 20px 'Segoe UI',Arial,sans-serif;color:#104E9D;padding-bottom:2px;">${nome}</td></tr>
        <tr><td style="font:400 13px Arial,sans-serif;color:#8ABE44;padding-bottom:8px;">${cargo}</td></tr>
        ${linhas.join('')}
      </table>
    </td>
    <td style="padding:0 0 0 18px;vertical-align:middle;">
      <img src="${logoSrc}" width="110" alt="SCI-AGRO" style="display:block;">
    </td>
  </tr>
  <tr><td colspan="3" style="padding-top:12px;"><span style="display:inline-block;background:#104E9D;color:#fff;font:600 11px Arial,sans-serif;padding:6px 12px;border-radius:0 0 6px 6px;">Your Product. Our Responsibility.</span></td></tr>
</table>`;
}

$('btn-export-html').addEventListener('click', () => {
  const code = buildSignatureHtml();
  $('html-code').value = code;
  $('html-output').classList.add('show');
});

$('btn-copy-html').addEventListener('click', () => {
  const ta = $('html-code');
  ta.select();
  navigator.clipboard && navigator.clipboard.writeText(ta.value).catch(()=>{});
  document.execCommand && document.execCommand('copy');
  const btn = $('btn-copy-html');
  const original = btn.textContent;
  btn.textContent = 'Copiado!';
  setTimeout(()=>{ btn.textContent = original; }, 1500);
});
</script>
<script>
__HTML2CANVAS__
</script>
</body>
</html>
"""

out = HTML.replace('__CARD_SVG__', CARD_SVG).replace('__HTML2CANVAS__', H2C).replace('__LOGO_EMAIL_B64__', LOGO_EMAIL_B64)

with open('index.html','w') as f:
    f.write(out)
print('written index.html', len(out), 'bytes')

artifact_out = (out
    .replace('<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n', '')
    .replace('<meta charset="UTF-8">\n', '')
    .replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n', '')
    .replace('<title>Gerador de Assinatura de E-mail — SCI-AGRO</title>\n', '<title>Assinatura SCI-AGRO</title>\n')
    .replace('</head>\n<body>\n', '\n')
    .replace('\n</body>\n</html>\n', '\n')
)
with open('artifact-content.html','w') as f:
    f.write(artifact_out)
print('written artifact-content.html', len(artifact_out), 'bytes')
